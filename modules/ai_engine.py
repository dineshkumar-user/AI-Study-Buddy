# ==========================================================
# AI ENGINE
# AI Study Buddy
#
# CLOUD:
#     Google Gemini API
#
# LOCAL:
#     Ollama + Llama 3.2 3B
#
# AI ROUTING:
#     1. Gemini 3.5 Flash-Lite
#     2. Gemini 3.6 Flash
#     3. Ollama Local AI
#
# Features:
#     - AI Chat
#     - Concept Explainer
#     - Smart Summary
#     - AI Quiz
#     - Flashcards
#     - Study Plan
#     - Learning Recommendations
#     - Automatic Gemini retry
#     - Gemini fallback
#     - Robust JSON parsing
#     - Quiz / flashcard retry
#     - Local fallback generation
# ==========================================================

import os
import json
import re
import time
from typing import Any, Optional


# ==========================================================
# OPTIONAL GEMINI IMPORT
# ==========================================================

try:
    from google import genai
except ImportError:
    genai = None


# ==========================================================
# CONFIGURATION
# ==========================================================

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2:3b"

# Gemini models configured for the project.
GEMINI_PRIMARY_MODEL = "gemini-3.5-flash-lite"
GEMINI_FALLBACK_MODEL = "gemini-3.6-flash"

GEMINI_RETRY_ATTEMPTS = 2
GEMINI_RETRY_DELAY = 4

# Keep prompts within a reasonable size for both cloud and local models.
MAX_NOTES_CHARS = 20000


# ==========================================================
# UTILITY HELPERS
# ==========================================================

def _clean_text(value: Any) -> str:
    """Convert a value to clean text."""
    if value is None:
        return ""
    return str(value).strip()


def _shorten_notes(notes: str, limit: int = MAX_NOTES_CHARS) -> str:
    """Limit study material sent to an AI model."""
    notes = _clean_text(notes)
    if len(notes) <= limit:
        return notes
    return notes[:limit] + "\n\n[Study material truncated here.]"


def _is_ai_error(response: Any) -> bool:
    """Return True when an AI response is one of our error responses."""
    if not response:
        return True

    text = str(response).strip()

    return (
        text.startswith("❌")
        or text.startswith("GEMINI_ERROR:")
        or text.startswith("OLLAMA_ERROR:")
    )


def _normalise_option_text(value: Any) -> str:
    """
    Normalize an answer/option so answers such as
    'A. Python' can match 'Python'.
    """
    text = _clean_text(value)

    text = re.sub(
        r"^\s*(?:option\s*)?[A-Da-d]\s*[\.\)\:\-]\s*",
        "",
        text,
        flags=re.IGNORECASE,
    )

    return text.strip()


# ==========================================================
# GEMINI API KEY
# ==========================================================

def get_gemini_key():
    """
    Get Gemini API key.

    Priority:
    1. Environment variable
    2. Streamlit Cloud secrets
    """

    api_key = os.getenv("GEMINI_API_KEY")

    if api_key:
        return str(api_key).strip()

    try:
        import streamlit as st

        try:
            api_key = st.secrets.get("GEMINI_API_KEY")

            if api_key:
                return str(api_key).strip()

        except Exception:
            pass

    except Exception:
        pass

    return None


# ==========================================================
# CHECK GEMINI AVAILABILITY
# ==========================================================

def gemini_available():
    """
    Return True when google-genai is installed and
    a Gemini API key is configured.
    """

    api_key = get_gemini_key()

    return (
        api_key is not None
        and api_key != ""
        and genai is not None
    )


# ==========================================================
# CREATE GEMINI CLIENT
# ==========================================================

def get_gemini_client():
    api_key = get_gemini_key()

    if not api_key or genai is None:
        return None

    try:
        return genai.Client(api_key=api_key)
    except Exception:
        return None


# ==========================================================
# GEMINI ERROR / RETRY HELPERS
# ==========================================================

def is_retryable_gemini_error(error):
    """Identify temporary Gemini/API errors."""
    error_text = str(error).upper()

    retryable_errors = (
        "429",
        "RESOURCE_EXHAUSTED",
        "500",
        "502",
        "503",
        "504",
        "UNAVAILABLE",
        "TIMEOUT",
        "DEADLINE",
        "INTERNAL",
        "OVERLOADED",
    )

    return any(code in error_text for code in retryable_errors)


def generate_gemini_response(client, model, prompt):
    """
    Generate a Gemini response with retry support.

    Returns:
        {
            "success": True,
            "text": "..."
        }

    or:
        {
            "success": False,
            "error": "...",
            "retryable": True/False
        }
    """

    last_error = "Unknown Gemini error."

    for attempt in range(GEMINI_RETRY_ATTEMPTS):
        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt,
            )

            text = getattr(response, "text", None)

            if text and str(text).strip():
                return {
                    "success": True,
                    "text": str(text).strip(),
                }

            last_error = "Gemini returned an empty response."

            # Empty responses are worth one retry.
            if attempt < GEMINI_RETRY_ATTEMPTS - 1:
                time.sleep(GEMINI_RETRY_DELAY)
                continue

        except Exception as error:
            last_error = str(error)

            if (
                is_retryable_gemini_error(error)
                and attempt < GEMINI_RETRY_ATTEMPTS - 1
            ):
                time.sleep(GEMINI_RETRY_DELAY)
                continue

            return {
                "success": False,
                "error": last_error,
                "retryable": is_retryable_gemini_error(error),
            }

    return {
        "success": False,
        "error": last_error,
        "retryable": True,
    }


# ==========================================================
# OLLAMA AI
# ==========================================================

def ask_ollama(prompt):
    """
    Ask the local Ollama server.

    Note:
    Ollama must be running on the same machine as the
    Streamlit process. Streamlit Cloud cannot normally
    access Ollama running on your personal computer.
    """

    try:
        import requests
    except ImportError:
        return (
            "OLLAMA_ERROR:"
            "The requests package is not installed."
        )

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.2,
                },
            },
            timeout=180,
        )

        response.raise_for_status()

        data = response.json()

        answer = data.get("response", "")

        if answer and str(answer).strip():
            return str(answer).strip()

        return (
            "OLLAMA_ERROR:"
            "Ollama returned an empty response."
        )

    except requests.exceptions.ConnectionError:
        return (
            "OLLAMA_ERROR:"
            "Local Ollama AI could not be reached. "
            "Make sure Ollama is running and that "
            "llama3.2:3b is installed."
        )

    except requests.exceptions.Timeout:
        return (
            "OLLAMA_ERROR:"
            "Ollama took too long to respond. "
            "Please try again."
        )

    except Exception as error:
        return (
            "OLLAMA_ERROR:"
            f"{error}"
        )


# ==========================================================
# GEMINI AI
# ==========================================================

def ask_gemini(prompt):
    """
    Cloud AI using Google Gemini.

    Routing:
        Primary Gemini
            ↓
        Fallback Gemini
            ↓
        return GEMINI_ERROR

    Ollama fallback is handled by ask_ai().
    """

    client = get_gemini_client()

    if client is None:
        return (
            "GEMINI_ERROR:"
            "Gemini client could not be created."
        )

    primary_result = generate_gemini_response(
        client,
        GEMINI_PRIMARY_MODEL,
        prompt,
    )

    if primary_result["success"]:
        return primary_result["text"]

    primary_error = primary_result["error"]

    fallback_result = generate_gemini_response(
        client,
        GEMINI_FALLBACK_MODEL,
        prompt,
    )

    if fallback_result["success"]:
        return fallback_result["text"]

    fallback_error = fallback_result["error"]

    return (
        "GEMINI_ERROR:\n\n"
        f"Primary model ({GEMINI_PRIMARY_MODEL}) failed:\n"
        f"{primary_error}\n\n"
        f"Fallback model ({GEMINI_FALLBACK_MODEL}) failed:\n"
        f"{fallback_error}"
    )


# ==========================================================
# UNIVERSAL AI ROUTER
# ==========================================================

def ask_ai(prompt):
    """
    Main AI router.

    Cloud:
        Gemini primary
            ↓
        Gemini fallback
            ↓
        Ollama

    Local:
        Ollama
    """

    if gemini_available():
        response = ask_gemini(prompt)

        if response and not response.startswith("GEMINI_ERROR:"):
            return response

        # Gemini failed; try local Ollama.
        ollama_response = ask_ollama(prompt)

        if (
            ollama_response
            and not ollama_response.startswith("OLLAMA_ERROR:")
        ):
            return ollama_response

        gemini_error = str(response).replace(
            "GEMINI_ERROR:",
            "",
        ).strip()

        ollama_error = str(ollama_response).replace(
            "OLLAMA_ERROR:",
            "",
        ).strip()

        return (
            "❌ Gemini AI Error\n\n"
            f"{gemini_error}\n\n"
            "⚠️ Local Ollama fallback is unavailable "
            "from the current environment.\n\n"
            f"Ollama details: {ollama_error}"
        )

    return ask_ollama(prompt)


# ==========================================================
# ROBUST JSON EXTRACTION
# ==========================================================

def _remove_markdown_fences(text: str) -> str:
    """Remove common Markdown code fences."""
    text = text.strip()

    text = re.sub(
        r"^\s*```(?:json|JSON)?\s*",
        "",
        text,
    )

    text = re.sub(
        r"\s*```\s*$",
        "",
        text,
    )

    return text.strip()


def _normalise_json_text(text: str) -> str:
    """Clean common formatting errors produced by small LLMs."""

    text = text.strip()

    # Smart quotes.
    text = (
        text.replace("\u201c", '"')
        .replace("\u201d", '"')
        .replace("\u2018", "'")
        .replace("\u2019", "'")
    )

    # Remove control characters except whitespace.
    text = re.sub(
        r"[\x00-\x08\x0b\x0c\x0e-\x1f]",
        "",
        text,
    )

    # Remove trailing commas before } or ].
    text = re.sub(
        r",\s*([}\]])",
        r"\1",
        text,
    )

    return text.strip()


def _extract_balanced_json(text: str, opening: str, closing: str):
    """
    Extract the first balanced JSON array/object.
    This is more reliable than simply using find('[') and rfind(']').
    """

    start = text.find(opening)

    if start == -1:
        return None

    depth = 0
    in_string = False
    escaped = False

    for index in range(start, len(text)):
        char = text[index]

        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False

            continue

        if char == '"':
            in_string = True
            continue

        if char == opening:
            depth += 1

        elif char == closing:
            depth -= 1

            if depth == 0:
                return text[start:index + 1]

    return None


def _try_json_loads(text: str):
    """Try normal JSON decoding after cleaning."""
    try:
        return json.loads(text)
    except Exception:
        return None


def clean_json_response(text):
    """
    Robustly convert an LLM response into Python JSON.

    Handles:
    - Markdown fences
    - Extra explanation before/after JSON
    - JSON arrays
    - JSON objects
    - Trailing commas
    - Smart quotes
    - Common wrapper objects
    """

    if not text:
        return None

    text = _remove_markdown_fences(str(text))
    text = _normalise_json_text(text)

    # First try the complete response.
    parsed = _try_json_loads(text)

    if parsed is not None:
        return parsed

    # Try a balanced JSON array.
    array_text = _extract_balanced_json(text, "[", "]")

    if array_text:
        array_text = _normalise_json_text(array_text)
        parsed = _try_json_loads(array_text)

        if parsed is not None:
            return parsed

    # Try a balanced JSON object.
    object_text = _extract_balanced_json(text, "{", "}")

    if object_text:
        object_text = _normalise_json_text(object_text)
        parsed = _try_json_loads(object_text)

        if parsed is not None:
            return parsed

    return None


# ==========================================================
# JSON WRAPPER EXTRACTION
# ==========================================================

def _extract_list_from_json(data, possible_keys):
    """
    Accept both:
        [...]
    and:
        {"quiz": [...]}
        {"questions": [...]}
        {"flashcards": [...]}
    """

    if isinstance(data, list):
        return data

    if isinstance(data, dict):
        for key in possible_keys:
            value = data.get(key)

            if isinstance(value, list):
                return value

        # Search one level deeper for a list.
        for value in data.values():
            if isinstance(value, list):
                return value

    return []


# ==========================================================
# CONCEPT EXPLAINER
# ==========================================================

def explain_concept(
    topic,
    notes="",
    difficulty="Simple - Beginner",
):
    prompt = f"""
You are an AI Study Buddy.

Explain the following concept to a student.

CONCEPT:
{topic}

STUDY MATERIAL:
{_shorten_notes(notes, 12000)}

EXPLANATION LEVEL:
{difficulty}

Instructions:
1. Explain clearly.
2. Use simple language.
3. Give a practical example.
4. Give an analogy when useful.
5. Mention important points.
6. Prioritize information from the study material.
7. Do not add unrelated information.

Format:

## 📚 Explanation

## 💡 Example

## 🧠 Important Points

## 🎯 Quick Memory Tip
"""

    return ask_ai(prompt)


# ==========================================================
# CHAT WITH NOTES
# ==========================================================

def chat_with_notes(question, notes):
    prompt = f"""
You are an AI Study Buddy.

Answer the student's question using the study
material provided below.

STUDY MATERIAL:
{_shorten_notes(notes, 16000)}

STUDENT QUESTION:
{question}

Instructions:
- Answer clearly.
- Use simple language.
- Stay relevant to the study material.
- Give an example when useful.
- If the answer is not present in the notes,
  clearly say that it is not available in the
  provided study material.
"""

    return ask_ai(prompt)


# ==========================================================
# AI SUMMARY
# ==========================================================

def generate_ai_summary(
    notes,
    summary_type="Bullet Points",
):
    if not _clean_text(notes):
        return "Please provide study material first."

    if summary_type == "Bullet Points":
        format_instruction = """
Create a bullet-point summary.

Include:
• Main concepts
• Important definitions
• Key facts
• Important examples
"""
    else:
        format_instruction = """
Create a clear paragraph summary.

Keep it concise while including the important concepts.
"""

    prompt = f"""
You are an AI Study Buddy.

Summarize the following study material.

STUDY MATERIAL:
{_shorten_notes(notes)}

{format_instruction}

Do not add information that is not supported
by the study material.
"""

    return ask_ai(prompt)


# ==========================================================
# BACKWARD COMPATIBILITY
# ==========================================================

def ai_summarize(notes, summary_type="Bullet Points"):
    return generate_ai_summary(notes, summary_type)


# ==========================================================
# QUIZ FALLBACK GENERATOR
# ==========================================================

def _make_fallback_quiz(notes, number):
    """
    Last-resort non-AI quiz generation.

    This prevents the UI from becoming completely unusable
    when an AI model returns malformed JSON.

    The generated questions are based only on sentences
    from the supplied notes.
    """

    sentences = re.split(
        r"(?<=[.!?])\s+|\n+",
        _clean_text(notes),
    )

    sentences = [
        re.sub(r"\s+", " ", s).strip()
        for s in sentences
        if len(re.sub(r"\s+", " ", s).strip()) >= 30
    ]

    if not sentences:
        return []

    questions = []

    for sentence in sentences:
        if len(questions) >= number:
            break

        words = re.findall(
            r"\b[A-Za-z][A-Za-z0-9_-]{3,}\b",
            sentence,
        )

        if len(words) < 2:
            continue

        answer = words[-1]
        question_text = (
            f"According to the study material, which term "
            f"appears in this statement: \"{sentence}\"?"
        )

        distractors = []

        for word in words[:-1]:
            candidate = word

            if (
                candidate.lower() != answer.lower()
                and candidate.lower() not in
                [d.lower() for d in distractors]
            ):
                distractors.append(candidate)

            if len(distractors) == 3:
                break

        while len(distractors) < 3:
            distractors.append(
                f"Not {len(distractors) + 1}"
            )

        options = [answer] + distractors[:3]

        # Rotate the correct answer so every question
        # does not always have the same position.
        rotation = len(questions) % 4
        options = options[rotation:] + options[:rotation]

        questions.append(
            {
                "question": question_text,
                "options": options,
                "answer": answer,
                "concept": "Study Material",
                "explanation": sentence,
            }
        )

    return questions[:number]


# ==========================================================
# QUIZ VALIDATION
# ==========================================================

def _validate_quiz_item(item):
    if not isinstance(item, dict):
        return None

    question = _clean_text(item.get("question"))
    options = item.get("options")
    answer = _clean_text(item.get("answer"))
    concept = _clean_text(item.get("concept")) or "General"
    explanation = _clean_text(item.get("explanation"))

    if not question or not isinstance(options, list):
        return None

    # Convert options to clean strings and remove empty values.
    cleaned_options = [
        _normalise_option_text(option)
        for option in options
        if _clean_text(option)
    ]

    # Remove duplicate options while preserving order.
    unique_options = []

    for option in cleaned_options:
        if option.lower() not in {
            x.lower() for x in unique_options
        }:
            unique_options.append(option)

    if len(unique_options) != 4:
        return None

    if not answer:
        return None

    # First: exact answer.
    matched_answer = None

    for option in unique_options:
        if option.lower() == answer.lower():
            matched_answer = option
            break

    # Second: remove A/B/C/D labels.
    if matched_answer is None:
        clean_answer = _normalise_option_text(answer)

        for option in unique_options:
            if (
                _normalise_option_text(option).lower()
                == clean_answer.lower()
            ):
                matched_answer = option
                break

    # Third: answer can sometimes be "A", "B", etc.
    if matched_answer is None:
        label_match = re.fullmatch(
            r"\s*([A-Da-d])\s*",
            answer,
        )

        if label_match:
            index = ord(label_match.group(1).upper()) - ord("A")

            if 0 <= index < len(unique_options):
                matched_answer = unique_options[index]

    if matched_answer is None:
        return None

    return {
        "question": question,
        "options": unique_options,
        "answer": matched_answer,
        "concept": concept,
        "explanation": explanation or "Review the study material for this concept.",
    }


# ==========================================================
# AI QUIZ GENERATOR
# ==========================================================

def generate_quiz(notes, number=5):
    if not _clean_text(notes):
        return []

    try:
        number = int(number)
    except Exception:
        number = 5

    number = max(3, min(number, 10))

    material = _shorten_notes(notes)

    prompt = f"""
You are an AI quiz generator.

Create exactly {number} multiple-choice questions
from the study material below.

STUDY MATERIAL:
{material}

RETURN FORMAT:
Return ONLY a JSON array. No Markdown. No explanation
before or after the JSON.

[
  {{
    "question": "Question text",
    "options": [
      "Option A",
      "Option B",
      "Option C",
      "Option D"
    ],
    "answer": "Correct option text",
    "concept": "Main concept",
    "explanation": "Short explanation"
  }}
]

STRICT RULES:
1. Create exactly {number} questions.
2. Every question must have exactly four options.
3. Only one option is correct.
4. The answer must be the exact text of the correct option.
5. Questions must be based only on the study material.
6. Avoid duplicate questions.
7. Cover different concepts when possible.
8. Do not put A., B., C., D. labels into option text.
9. Return valid JSON.
"""

    response = ask_ai(prompt)

    if _is_ai_error(response):
        return _make_fallback_quiz(notes, number)

    quiz_data = clean_json_response(response)

    quiz_items = _extract_list_from_json(
        quiz_data,
        [
            "quiz",
            "questions",
            "mcqs",
            "items",
            "data",
        ],
    )

    valid_questions = []

    for item in quiz_items:
        validated = _validate_quiz_item(item)

        if validated is not None:
            # Avoid duplicate questions.
            normalized_question = re.sub(
                r"\s+",
                " ",
                validated["question"].lower(),
            )

            existing = {
                re.sub(
                    r"\s+",
                    " ",
                    q["question"].lower(),
                )
                for q in valid_questions
            }

            if normalized_question not in existing:
                valid_questions.append(validated)

        if len(valid_questions) >= number:
            break

    # ------------------------------------------------------
    # If parsing/validation failed, ask the model once more
    # to convert its previous output into strict JSON.
    # ------------------------------------------------------

    if len(valid_questions) < number:
        repair_prompt = f"""
Convert the following AI-generated quiz into valid JSON.

Return ONLY a JSON array.

You MUST return exactly {number} objects.

Each object MUST contain:
question
options
answer
concept
explanation

Each options array MUST contain exactly four strings.
The answer MUST exactly match one option.

ORIGINAL RESPONSE:
{str(response)[:16000]}
"""

        repaired_response = ask_ai(repair_prompt)

        repaired_data = clean_json_response(repaired_response)

        repaired_items = _extract_list_from_json(
            repaired_data,
            [
                "quiz",
                "questions",
                "mcqs",
                "items",
                "data",
            ],
        )

        for item in repaired_items:
            validated = _validate_quiz_item(item)

            if validated is None:
                continue

            normalized_question = re.sub(
                r"\s+",
                " ",
                validated["question"].lower(),
            )

            existing = {
                re.sub(
                    r"\s+",
                    " ",
                    q["question"].lower(),
                )
                for q in valid_questions
            }

            if normalized_question not in existing:
                valid_questions.append(validated)

            if len(valid_questions) >= number:
                break

    # ------------------------------------------------------
    # Last resort: deterministic quiz from notes.
    # ------------------------------------------------------

    if not valid_questions:
        return _make_fallback_quiz(notes, number)

    return valid_questions[:number]


# ==========================================================
# FLASHCARD VALIDATION
# ==========================================================

def _validate_flashcard(item):
    if not isinstance(item, dict):
        return None

    question = _clean_text(item.get("question"))
    answer = _clean_text(item.get("answer"))
    concept = _clean_text(item.get("concept")) or "General"

    if not question or not answer:
        return None

    return {
        "question": question,
        "answer": answer,
        "concept": concept,
    }


# ==========================================================
# FLASHCARD FALLBACK GENERATOR
# ==========================================================

def _make_fallback_flashcards(notes, number):
    """
    Last-resort flashcard generation from note sentences.
    """

    sentences = re.split(
        r"(?<=[.!?])\s+|\n+",
        _clean_text(notes),
    )

    cards = []

    for sentence in sentences:
        sentence = re.sub(r"\s+", " ", sentence).strip()

        if len(sentence) < 25:
            continue

        words = re.findall(
            r"\b[A-Za-z][A-Za-z0-9_-]{3,}\b",
            sentence,
        )

        if not words:
            continue

        concept = words[0]

        cards.append(
            {
                "question": f"What is important to remember from this statement about {concept}?",
                "answer": sentence,
                "concept": concept,
            }
        )

        if len(cards) >= number:
            break

    return cards


# ==========================================================
# AI FLASHCARD GENERATOR
# ==========================================================

def generate_flashcards(notes, number=5):
    if not _clean_text(notes):
        return []

    try:
        number = int(number)
    except Exception:
        number = 5

    number = max(3, min(number, 15))

    material = _shorten_notes(notes)

    prompt = f"""
You are an AI flashcard generator.

Create exactly {number} useful revision flashcards
from the study material below.

STUDY MATERIAL:
{material}

RETURN FORMAT:
Return ONLY a JSON array. No Markdown. No explanation.

[
  {{
    "question": "Question",
    "answer": "Answer",
    "concept": "Concept"
  }}
]

STRICT RULES:
1. Create exactly {number} cards.
2. Questions must be useful for revision.
3. Answers must be concise and accurate.
4. Cover different concepts when possible.
5. Do not duplicate questions.
6. Use only information supported by the study material.
7. Return valid JSON.
"""

    response = ask_ai(prompt)

    if _is_ai_error(response):
        return _make_fallback_flashcards(notes, number)

    card_data = clean_json_response(response)

    card_items = _extract_list_from_json(
        card_data,
        [
            "flashcards",
            "cards",
            "items",
            "data",
        ],
    )

    valid_cards = []

    for item in card_items:
        validated = _validate_flashcard(item)

        if validated is None:
            continue

        normalized_question = re.sub(
            r"\s+",
            " ",
            validated["question"].lower(),
        )

        existing = {
            re.sub(
                r"\s+",
                " ",
                card["question"].lower(),
            )
            for card in valid_cards
        }

        if normalized_question not in existing:
            valid_cards.append(validated)

        if len(valid_cards) >= number:
            break

    # ------------------------------------------------------
    # One repair attempt.
    # ------------------------------------------------------

    if len(valid_cards) < number:
        repair_prompt = f"""
Convert the following AI-generated flashcards into valid JSON.

Return ONLY a JSON array.

Return exactly {number} objects.

Each object MUST contain:
question
answer
concept

ORIGINAL RESPONSE:
{str(response)[:16000]}
"""

        repaired_response = ask_ai(repair_prompt)

        repaired_data = clean_json_response(repaired_response)

        repaired_items = _extract_list_from_json(
            repaired_data,
            [
                "flashcards",
                "cards",
                "items",
                "data",
            ],
        )

        for item in repaired_items:
            validated = _validate_flashcard(item)

            if validated is None:
                continue

            normalized_question = re.sub(
                r"\s+",
                " ",
                validated["question"].lower(),
            )

            existing = {
                re.sub(
                    r"\s+",
                    " ",
                    card["question"].lower(),
                )
                for card in valid_cards
            }

            if normalized_question not in existing:
                valid_cards.append(validated)

            if len(valid_cards) >= number:
                break

    if not valid_cards:
        return _make_fallback_flashcards(notes, number)

    return valid_cards[:number]


# ==========================================================
# STUDY PLAN
# ==========================================================

def generate_study_plan(weak_topics, study_hours=2):
    if not weak_topics:
        weak_topics = ["General revision"]

    topics_text = "\n".join(
        f"- {topic}"
        for topic in weak_topics
    )

    prompt = f"""
You are an AI personal study planner.

Create a personalized study plan.

WEAK TOPICS:
{topics_text}

AVAILABLE STUDY TIME:
{study_hours} hours per day

Create a practical plan.

Include:

## 📅 Daily Schedule
## 🎯 Priority Topics
## 📝 Practice Activities
## 🔄 Revision Strategy
## 🏆 Goal

Keep the plan realistic for a student.
"""

    return ask_ai(prompt)


# ==========================================================
# LEARNING RECOMMENDATION
# ==========================================================

def generate_learning_recommendation(weak_topics, score=0):
    if weak_topics:
        topics_text = ", ".join(
            str(topic)
            for topic in weak_topics
        )
    else:
        topics_text = "No weak topics recorded."

    prompt = f"""
You are an AI learning advisor.

Student latest quiz score:
{score}%

Weak concepts:
{topics_text}

Provide personalized recommendations.

Include:
1. What the student is doing well.
2. What needs improvement.
3. Which topics to study first.
4. Recommended practice activities.
5. A short motivation message.

Keep the response concise.
"""

    return ask_ai(prompt)


# ==========================================================
# AI MODE
# ==========================================================

def get_ai_mode():
    if gemini_available():
        return "☁️ Gemini Cloud AI"

    return "💻 Ollama Local AI"


# ==========================================================
# AI STATUS
# ==========================================================

def get_ai_status():
    if gemini_available():
        return {
            "mode": "Gemini",
            "model": GEMINI_PRIMARY_MODEL,
            "status": "Connected",
        }

    return {
        "mode": "Ollama",
        "model": OLLAMA_MODEL,
        "status": "Local mode",
    }


# ==========================================================
# OPTIONAL DIAGNOSTIC FUNCTION
# ==========================================================

def get_ai_diagnostics():
    """
    Useful for debugging from the Streamlit app or Python shell.
    Does not expose the API key.
    """

    diagnostics = {
        "gemini_package_installed": genai is not None,
        "gemini_key_configured": bool(get_gemini_key()),
        "gemini_primary_model": GEMINI_PRIMARY_MODEL,
        "gemini_fallback_model": GEMINI_FALLBACK_MODEL,
        "ollama_url": OLLAMA_URL,
        "ollama_model": OLLAMA_MODEL,
    }

    return diagnostics
