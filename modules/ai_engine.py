import requests
import json
import re


# ============================================================
# OLLAMA CONFIGURATION
# ============================================================

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:3b"


# ============================================================
# BASIC OLLAMA FUNCTION
# ============================================================

def ask_ollama(prompt):

    try:

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False
            },
            timeout=180
        )

        response.raise_for_status()

        data = response.json()

        return data.get("response", "").strip()

    except requests.exceptions.ConnectionError:

        return (
            "ERROR: Ollama is not running. "
            "Please start Ollama and try again."
        )

    except Exception as error:

        return f"ERROR: {error}"


# ============================================================
# CONCEPT EXPLAINER
# ============================================================

def explain_concept(
    topic,
    notes="",
    difficulty="Simple - Beginner"
):

    if notes:

        context = notes[:8000]

    else:

        context = "No study notes provided."

    prompt = f"""
You are an AI Study Buddy.

Explain the following concept to a student.

CONCEPT:
{topic}

STUDY MATERIAL:
{context}

EXPLANATION LEVEL:
{difficulty}

Give the answer using this structure:

## 📌 Simple Definition

## 🧠 Explanation

## 💡 Example

## 🔑 Key Points

Keep the explanation educational and easy to understand.
"""

    return ask_ollama(prompt)


# ============================================================
# CHAT WITH NOTES
# ============================================================

def chat_with_notes(
    question,
    notes
):

    prompt = f"""
You are an AI Study Buddy.

Answer the student's question using the study material below.

STUDY MATERIAL:
{notes[:12000]}

QUESTION:
{question}

Instructions:

1. Give a clear answer.
2. Explain difficult terms simply.
3. Use examples when useful.
4. If the answer is not present in the notes, say so.
5. Do not invent information from the notes.

Answer:
"""

    return ask_ollama(prompt)


# ============================================================
# AI SUMMARY
# ============================================================

def ai_summarize(
    notes,
    summary_type="Bullet Points"
):

    if summary_type == "Bullet Points":

        instruction = """
Create a concise bullet-point summary.
Highlight the most important concepts, definitions,
examples and key facts.
"""

    else:

        instruction = """
Create a concise paragraph summary.
Include the most important concepts and facts.
"""

    prompt = f"""
You are an AI Study Buddy.

Summarize the following study material.

STUDY MATERIAL:
{notes[:12000]}

{instruction}

Do not add information that is not present in the study material.
"""

    return ask_ollama(prompt)


# ============================================================
# COMPATIBILITY ALIAS
# ============================================================

def generate_ai_summary(
    notes,
    summary_type="Bullet Points"
):

    return ai_summarize(
        notes,
        summary_type
    )


# ============================================================
# CLEAN JSON RESPONSE
# ============================================================

def extract_json(text):

    text = text.strip()

    # Remove markdown code fences
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

    # Find JSON array
    start = text.find("[")

    end = text.rfind("]")

    if start != -1 and end != -1:

        text = text[start:end + 1]

    try:

        return json.loads(text)

    except json.JSONDecodeError:

        return None


# ============================================================
# AI QUIZ GENERATOR
# ============================================================

def generate_quiz(
    notes,
    number=5
):

    prompt = f"""
You are an AI quiz generator.

Create exactly {number} multiple-choice questions
from the study material below.

STUDY MATERIAL:
{notes[:12000]}

IMPORTANT:
Return ONLY valid JSON.

Do not use markdown.
Do not write explanations before or after the JSON.

The JSON must have exactly this structure:

[
  {{
    "question": "Question text",
    "options": [
      "A. option",
      "B. option",
      "C. option",
      "D. option"
    ],
    "answer": "A. option",
    "concept": "Main concept",
    "explanation": "Short explanation"
  }}
]

Rules:

1. Exactly {number} questions.
2. Every question must have exactly 4 options.
3. The answer MUST exactly match one of the options.
4. Questions must be based only on the study material.
5. Make questions educational.
6. Avoid duplicate questions.
7. Include a useful concept name.
8. Include a short explanation.
"""

    raw_response = ask_ollama(prompt)

    if raw_response.startswith("ERROR:"):

        return []

    quiz = extract_json(raw_response)

    if not isinstance(quiz, list):

        return []

    valid_quiz = []

    for item in quiz:

        if not isinstance(item, dict):

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

        if (
            question
            and isinstance(options, list)
            and len(options) == 4
            and answer in options
        ):

            valid_quiz.append({
                "question": question,
                "options": options,
                "answer": answer,
                "concept": concept,
                "explanation": explanation
            })

    return valid_quiz[:number]


# ============================================================
# COMPATIBILITY FUNCTION
# ============================================================

def generate_ai_quiz(
    notes,
    number=5
):

    return generate_quiz(
        notes,
        number
    )


# ============================================================
# AI FLASHCARD GENERATOR
# ============================================================

def generate_flashcards(
    notes,
    number=5
):

    prompt = f"""
You are an AI flashcard generator.

Create exactly {number} useful study flashcards
from the following study material.

STUDY MATERIAL:
{notes[:12000]}

Return ONLY valid JSON.

Do not use markdown.
Do not write anything outside the JSON.

Required format:

[
  {{
    "question": "What is ...?",
    "answer": "Clear answer",
    "concept": "Main concept"
  }}
]

Rules:

1. Exactly {number} flashcards.
2. Questions must be useful for revision.
3. Answers must be concise but informative.
4. Questions must be based only on the study material.
5. Avoid duplicate flashcards.
6. Include a concept for every card.
"""

    raw_response = ask_ollama(prompt)

    if raw_response.startswith("ERROR:"):

        return []

    cards = extract_json(raw_response)

    if not isinstance(cards, list):

        return []

    valid_cards = []

    for card in cards:

        if not isinstance(card, dict):

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
                "question": question,
                "answer": answer,
                "concept": concept
            })

    return valid_cards[:number]


# ============================================================
# AI STUDY PLAN
# ============================================================

def generate_study_plan(
    weak_topics,
    study_time
):

    prompt = f"""
You are an AI Study Planner.

Create a personalized study plan.

WEAK TOPICS:
{weak_topics}

AVAILABLE STUDY TIME:
{study_time}

Create:

## 📅 Study Plan

## 🎯 Priority Topics

## ⏰ Time Allocation

## 📝 Recommended Activities

## 🔄 Revision Strategy

Keep the plan practical for a student.
"""

    return ask_ollama(prompt)


# ============================================================
# COMPATIBILITY FUNCTION
# ============================================================

def create_study_plan(
    weak_topics,
    study_time
):

    return generate_study_plan(
        weak_topics,
        study_time
    )


# ============================================================
# LEARNING RECOMMENDATION
# ============================================================

def generate_learning_recommendation(
    score,
    weak_topics
):

    prompt = f"""
You are an AI learning coach.

Student quiz score:
{score}%

Weak topics:
{weak_topics}

Give personalized recommendations.

Include:

1. Performance analysis
2. Topics to revise
3. Recommended study activities
4. Suggested next quiz difficulty
5. Motivation

Keep the response concise and useful.
"""

    return ask_ollama(prompt)


# ============================================================
# SIMPLE AI RECOMMENDATION
# ============================================================

def get_learning_recommendation(
    score,
    weak_topics
):

    return generate_learning_recommendation(
        score,
        weak_topics
    )