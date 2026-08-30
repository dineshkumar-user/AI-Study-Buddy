# ==========================================================
# AI ENGINE
# AI Study Buddy
#
# LOCAL:
#     Ollama + Llama 3.2
#
# CLOUD:
#     Google Gemini API
# ==========================================================

import os
import json
import re


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

OLLAMA_MODEL = "llama3.2:3b"

# Gemini model
GEMINI_MODEL = "gemini-2.5-flash"


# ==========================================================
# GET GEMINI API KEY
# ==========================================================

def get_gemini_key():

    # ------------------------------------------------------
    # 1. Environment variable
    # ------------------------------------------------------

    api_key = os.getenv("GEMINI_API_KEY")

    if api_key:
        return api_key.strip()


    # ------------------------------------------------------
    # 2. Streamlit Secrets
    # ------------------------------------------------------

    try:

        import streamlit as st

        api_key = st.secrets.get(
            "GEMINI_API_KEY",
            None
        )

        if api_key:
            return str(api_key).strip()

    except Exception:

        pass


    return None


# ==========================================================
# CHECK GEMINI AVAILABILITY
# ==========================================================

def gemini_available():

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
# DETECT CLOUD / LOCAL ENVIRONMENT
# ==========================================================

def is_streamlit_cloud():

    """
    Detect whether the application is running
    on Streamlit Cloud.
    """

    # Streamlit Cloud normally provides this environment variable
    if os.getenv("STREAMLIT_RUNTIME_ENV"):

        return True

    # Additional Streamlit Cloud indicators
    if os.getenv("HOSTNAME", "").startswith("streamlit"):

        return True

    # If Gemini key exists, prefer Gemini.
    # This is useful for cloud deployment.
    if get_gemini_key():

        return True

    return False


# ==========================================================
# OLLAMA AI
# ==========================================================

def ask_ollama(prompt):

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

        result = data.get(
            "response",
            ""
        )

        if result:

            return result.strip()

        return "Ollama returned an empty response."

    except Exception as error:

        return (
            "AI Error: Ollama could not be reached.\n\n"
            f"{error}"
        )


# ==========================================================
# GEMINI AI
# ==========================================================

def ask_gemini(prompt):

    client = get_gemini_client()

    if client is None:

        return (
            "GEMINI_ERROR: "
            "Gemini client is not available. "
            "Check GEMINI_API_KEY and google-genai installation."
        )

    try:

        response = client.models.generate_content(

            model=GEMINI_MODEL,

            contents=prompt
        )

        if response and response.text:

            return response.text.strip()

        return (
            "GEMINI_ERROR: "
            "Gemini returned an empty response."
        )

    except Exception as error:

        return (
            "GEMINI_ERROR: "
            f"{error}"
        )


# ==========================================================
# UNIVERSAL AI FUNCTION
# ==========================================================

def ask_ai(prompt):

    """
    AI selection:

    CLOUD:
        Gemini

    LOCAL:
        Ollama

    If Gemini is available, Gemini is always preferred.
    """

    # ------------------------------------------------------
    # CLOUD / GEMINI MODE
    # ------------------------------------------------------

    if gemini_available():

        response = ask_gemini(prompt)

        if response and not response.startswith(
            "GEMINI_ERROR:"
        ):

            return response

        # IMPORTANT:
        # Do NOT fall back to Ollama in cloud.
        # Streamlit Cloud cannot access localhost Ollama.

        return (
            "❌ Gemini AI Error\n\n"
            f"{response}"
        )


    # ------------------------------------------------------
    # LOCAL MODE
    # ------------------------------------------------------

    return ask_ollama(prompt)


# ==========================================================
# CLEAN JSON RESPONSE
# ==========================================================

def clean_json_response(text):

    if not text:

        return None

    text = text.strip()


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
            start:
            end + 1
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
                start:
                end + 1
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

Answer the student's question using the study
material provided below.

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
  clearly say that it is not available in the
  provided study material.
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

Rules:

1. Exactly {number} questions.
2. Exactly four options per question.
3. Only one correct answer.
4. The answer must exactly match one of the options.
5. Questions must be based on the study material.
6. Avoid duplicate questions.
7. Make questions educational.
8. Do not include A., B., C., D. labels inside options.
"""


    response = ask_ai(prompt)


    # If AI failed
    if (
        not response
        or response.startswith("❌ Gemini AI Error")
        or response.startswith("AI Error:")
    ):

        return []


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
        # Convert options to strings
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


        valid_questions.append({

            "question":
                question,

            "options":
                options,

            "answer":
                answer,

            "concept":
                concept,

            "explanation":
                explanation
        })


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


    if (
        not response
        or response.startswith("❌ Gemini AI Error")
        or response.startswith("AI Error:")
    ):

        return []


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

            valid_cards.append({

                "question":
                    str(question).strip(),

                "answer":
                    str(answer).strip(),

                "concept":
                    str(concept).strip()
            })


    return valid_cards[:number]


# ==========================================================
# STUDY PLAN
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
# LEARNING RECOMMENDATION
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

        return "☁️ Gemini AI"

    return "💻 Ollama Local AI"


# ==========================================================
# AI STATUS
# ==========================================================

def get_ai_status():

    if gemini_available():

        return {

            "mode":
                "Gemini",

            "model":
                GEMINI_MODEL,

            "status":
                "Connected"
        }


    return {

        "mode":
            "Ollama",

        "model":
            OLLAMA_MODEL,

        "status":
            "Local mode"
    }