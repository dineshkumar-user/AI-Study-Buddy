# ==========================================================
# 🎓 AI STUDY BUDDY - AI ENGINE
#
# CLOUD AI:
#   Google Gemini
#
# LOCAL AI:
#   Ollama + Llama 3.2 3B
#
# Priority:
#   1. Gemini Cloud AI when GEMINI_API_KEY exists
#   2. Ollama Local AI otherwise
#
# ==========================================================

import os
import json
import re

# ==========================================================
# GEMINI IMPORT
# ==========================================================

try:
    from google import genai
except ImportError:
    genai = None


# ==========================================================
# CONFIGURATION
# ==========================================================

OLLAMA_MODEL = "llama3.2:3b"

# Cloud model
GEMINI_MODEL = "gemini-2.5-flash"


# ==========================================================
# GET GEMINI API KEY
# ==========================================================

def get_gemini_key():
    """
    Get Gemini API key.

    Priority:
    1. Environment variable
    2. Streamlit secrets
    """

    # ------------------------------------------------------
    # 1. Environment variable
    # ------------------------------------------------------

    api_key = os.getenv("GEMINI_API_KEY")

    if api_key:
        return str(api_key).strip()

    # ------------------------------------------------------
    # 2. Streamlit Cloud secrets
    # ------------------------------------------------------

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
    Returns True when Gemini can be used.
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
    """
    Create Google Gemini client.
    """

    api_key = get_gemini_key()

    if not api_key:
        return None

    if genai is None:
        return None

    try:
        client = genai.Client(
            api_key=api_key
        )

        return client

    except Exception:
        return None


# ==========================================================
# LOCAL OLLAMA AI
# ==========================================================

def ask_ollama(prompt):
    """
    Local AI using Ollama.

    Used when:
    - Running locally
    - Gemini API key is not available
    """

    try:

        import requests

        response = requests.post(
            "http://localhost:11434/api/generate",

            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False
            },

            timeout=180
        )

        response.raise_for_status()

        data = response.json()

        answer = data.get(
            "response",
            ""
        )

        if answer:
            return answer.strip()

        return (
            "❌ Ollama returned an empty response."
        )

    except Exception as error:

        return (
            "❌ Local Ollama AI could not be reached.\n\n"
            "If you are running the application locally, "
            "make sure Ollama is installed and running.\n\n"
            f"Details: {error}"
        )


# ==========================================================
# GEMINI CLOUD AI
# ==========================================================

def ask_gemini(prompt):
    """
    Cloud AI using Google Gemini.
    """

    client = get_gemini_client()

    if client is None:
        return None

    try:

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )

        if response is not None:

            text = getattr(
                response,
                "text",
                None
            )

            if text:
                return text.strip()

        return None

    except Exception as error:

        return (
            "GEMINI_ERROR:"
            + str(error)
        )


# ==========================================================
# UNIVERSAL AI ROUTER
# ==========================================================

def ask_ai(prompt):
    """
    Main AI router.

    Cloud:
        Gemini

    Local:
        Ollama
    """

    # ======================================================
    # GEMINI CLOUD
    # ======================================================

    if gemini_available():

        response = ask_gemini(prompt)

        if response:

            if response.startswith(
                "GEMINI_ERROR:"
            ):

                return (
                    "❌ Gemini AI Error\n\n"
                    + response.replace(
                        "GEMINI_ERROR:",
                        ""
                    )
                )

            return response

        return (
            "❌ Gemini returned no response."
        )

    # ======================================================
    # OLLAMA LOCAL
    # ======================================================

    return ask_ollama(prompt)


# ==========================================================
# CLEAN JSON RESPONSE
# ==========================================================

def clean_json_response(text):
    """
    Clean AI response and convert it into JSON.
    """

    if not text:
        return None

    text = str(text).strip()

    # ------------------------------------------------------
    # Remove markdown code blocks
    # ------------------------------------------------------

    text = re.sub(
        r"```json",
        "",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"```",
        "",
        text
    )

    text = text.strip()

    # ------------------------------------------------------
    # Find JSON array
    # ------------------------------------------------------

    start = text.find("[")
    end = text.rfind("]")

    if (
        start != -1
        and end != -1
        and end > start
    ):

        text = text[
            start:end + 1
        ]

    else:

        # --------------------------------------------------
        # Find JSON object
        # --------------------------------------------------

        start = text.find("{")
        end = text.rfind("}")

        if (
            start != -1
            and end != -1
            and end > start
        ):

            text = text[
                start:end + 1
            ]

    # ------------------------------------------------------
    # Parse JSON
    # ------------------------------------------------------

    try:

        return json.loads(text)

    except Exception:

        return None


# ==========================================================
# CONCEPT EXPLAINER
# ==========================================================

def explain_concept(
    topic,
    notes="",
    difficulty="Simple - Beginner"
):

    prompt = f"""
You are an AI Study Buddy.

Explain the following concept to a student.

CONCEPT:
{topic}

STUDY MATERIAL:
{notes[:12000]}

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

def chat_with_notes(
    question,
    notes
):

    prompt = f"""
You are an AI Study Buddy.

Answer the student's question using the
study material provided below.

STUDY MATERIAL:

{notes[:16000]}

STUDENT QUESTION:

{question}

Instructions:

- Answer clearly.
- Use simple language.
- Stay relevant to the study material.
- Give an example when useful.
- If the answer is not present in the notes,
  clearly say that it is not available in
  the provided study material.
"""

    return ask_ai(prompt)


# ==========================================================
# AI SUMMARY
# ==========================================================

def generate_ai_summary(
    notes,
    summary_type="Bullet Points"
):

    if not notes.strip():

        return (
            "Please provide study material first."
        )

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

Keep it concise while including the
important concepts.
"""

    prompt = f"""
You are an AI Study Buddy.

Summarize the following study material.

STUDY MATERIAL:

{notes[:20000]}

{format_instruction}

Do not add information that is not supported
by the study material.
"""

    return ask_ai(prompt)


# ==========================================================
# BACKWARD COMPATIBILITY
# ==========================================================

def ai_summarize(
    notes,
    summary_type="Bullet Points"
):

    return generate_ai_summary(
        notes,
        summary_type
    )


# ==========================================================
# AI QUIZ GENERATOR
# ==========================================================

def generate_quiz(
    notes,
    number=5
):

    if not notes.strip():
        return []

    number = max(
        3,
        min(number, 10)
    )

    prompt = f"""
You are an AI quiz generator.

Create exactly {number} multiple-choice
questions from the study material below.

STUDY MATERIAL:

{notes[:20000]}

IMPORTANT:

Return ONLY valid JSON.

Do NOT use markdown.

Do NOT write anything before or after
the JSON.

Return exactly this structure:

[
  {{
    "question": "Question text",
    "options": [
      "Option A text",
      "Option B text",
      "Option C text",
      "Option D text"
    ],
    "answer": "Correct option text",
    "concept": "Main concept",
    "explanation": "Short explanation"
  }}
]

Rules:

1. Exactly {number} questions.
2. Exactly four options per question.
3. Only one correct answer.
4. The answer must exactly match one
   of the options.
5. Questions must be based on the
   study material.
6. Avoid duplicate questions.
7. Make questions educational.
8. Do not include A., B., C., D.
   inside the option text.
9. Do not include "Correct Answer"
   in the question.
10. Return pure JSON only.
"""

    response = ask_ai(prompt)

    quiz = clean_json_response(
        response
    )

    if not isinstance(
        quiz,
        list
    ):
        return []

    valid_questions = []

    for item in quiz:

        if not isinstance(
            item,
            dict
        ):
            continue

        question = item.get(
            "question",
            ""
        )

        options = item.get(
            "options",
            []
        )

        answer = item.get(
            "answer",
            ""
        )

        concept = item.get(
            "concept",
            "General"
        )

        explanation = item.get(
            "explanation",
            ""
        )

        # --------------------------------------------------
        # Validate
        # --------------------------------------------------

        if not question:
            continue

        if not isinstance(
            options,
            list
        ):
            continue

        if len(options) != 4:
            continue

        if not answer:
            continue

        # --------------------------------------------------
        # Convert to strings
        # --------------------------------------------------

        options = [
            str(option).strip()
            for option in options
        ]

        answer = str(answer).strip()

        # --------------------------------------------------
        # Match answer with option
        # --------------------------------------------------

        if answer not in options:

            matched_answer = None

            clean_answer = re.sub(
                r"^[A-Da-d][\.\)\:\-]\s*",
                "",
                answer
            ).strip()

            for option in options:

                clean_option = re.sub(
                    r"^[A-Da-d][\.\)\:\-]\s*",
                    "",
                    option
                ).strip()

                if (
                    clean_option.lower()
                    ==
                    clean_answer.lower()
                ):

                    matched_answer = option
                    break

            if matched_answer:

                answer = matched_answer

            else:

                continue

        valid_questions.append(
            {
                "question": str(question),
                "options": options,
                "answer": answer,
                "concept": str(concept),
                "explanation": str(explanation)
            }
        )

    return valid_questions[:number]


# ==========================================================
# AI FLASHCARD GENERATOR
# ==========================================================

def generate_flashcards(
    notes,
    number=5
):

    if not notes.strip():
        return []

    number = max(
        3,
        min(number, 15)
    )

    prompt = f"""
You are an AI flashcard generator.

Create exactly {number} flashcards from
the study material.

STUDY MATERIAL:

{notes[:20000]}

IMPORTANT:

Return ONLY valid JSON.

Do NOT use markdown.

Do NOT write anything before or after
the JSON.

Return exactly:

[
  {{
    "question": "Question",
    "answer": "Answer",
    "concept": "Concept"
  }}
]

Rules:

1. Exactly {number} cards.
2. Questions must be useful for revision.
3. Answers must be concise and accurate.
4. Cover different concepts.
5. Do not duplicate questions.
6. Use only information supported
   by the study material.
"""

    response = ask_ai(prompt)

    cards = clean_json_response(
        response
    )

    if not isinstance(
        cards,
        list
    ):
        return []

    valid_cards = []

    for card in cards:

        if not isinstance(
            card,
            dict
        ):
            continue

        question = card.get(
            "question",
            ""
        )

        answer = card.get(
            "answer",
            ""
        )

        concept = card.get(
            "concept",
            "General"
        )

        if question and answer:

            valid_cards.append(
                {
                    "question": str(question),
                    "answer": str(answer),
                    "concept": str(concept)
                }
            )

    return valid_cards[:number]


# ==========================================================
# AI STUDY PLAN
# ==========================================================

def generate_study_plan(
    weak_topics,
    study_hours=2
):

    if not weak_topics:

        weak_topics = [
            "General revision"
        ]

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
# AI LEARNING RECOMMENDATION
# ==========================================================

def generate_learning_recommendation(
    weak_topics,
    score=0
):

    if weak_topics:

        topics_text = ", ".join(
            weak_topics
        )

    else:

        topics_text = (
            "No weak topics recorded."
        )

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
            "model": GEMINI_MODEL,
            "status": "Connected"
        }

    return {
        "mode": "Ollama",
        "model": OLLAMA_MODEL,
        "status": "Local mode"
    }


# ==========================================================
# END OF AI ENGINE
# ==========================================================