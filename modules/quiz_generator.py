import json
import re
from modules.ai_engine import ask_ollama


def clean_json_response(response):
    """
    Extract JSON from the Ollama response.
    Handles responses containing markdown code blocks.
    """

    response = response.strip()

    # Remove ```json and ```
    response = re.sub(r"```json", "", response, flags=re.IGNORECASE)
    response = re.sub(r"```", "", response)

    response = response.strip()

    # Find JSON array
    start = response.find("[")
    end = response.rfind("]")

    if start != -1 and end != -1:
        response = response[start:end + 1]

    return response


def validate_question(question):
    """
    Validate and clean one quiz question.
    """

    if not isinstance(question, dict):
        return None

    required_fields = [
        "question",
        "options",
        "answer",
        "concept",
        "explanation"
    ]

    for field in required_fields:
        if field not in question:
            return None

    if not isinstance(question["options"], list):
        return None

    if len(question["options"]) != 4:
        return None

    options = [
        str(option).strip()
        for option in question["options"]
    ]

    answer = str(question["answer"]).strip()

    # Make sure answer exists in options
    if answer not in options:

        # Handle answers such as "B. Something"
        for option in options:

            if answer.lower() in option.lower():
                answer = option
                break

    if answer not in options:
        return None

    return {
        "question": str(question["question"]).strip(),
        "options": options,
        "answer": answer,
        "concept": str(question["concept"]).strip(),
        "explanation": str(question["explanation"]).strip()
    }


def generate_quiz(notes, number=5):

    if not notes or not notes.strip():
        return []

    prompt = f"""
You are an educational quiz generator.

Create exactly {number} multiple-choice questions from the study material below.

IMPORTANT:
Return ONLY valid JSON.
Do NOT write explanations outside the JSON.
Do NOT use markdown.
Do NOT write "Here are the questions".
Do NOT number the questions outside JSON.

Each question MUST have exactly this structure:

[
  {{
    "question": "Question text",
    "options": [
      "Option 1",
      "Option 2",
      "Option 3",
      "Option 4"
    ],
    "answer": "The exact correct option text",
    "concept": "Main concept",
    "explanation": "Short explanation of why the answer is correct"
  }}
]

Rules:
- Exactly 4 options.
- Only one correct answer.
- The answer must exactly match one option.
- Questions must be based ONLY on the supplied study material.
- Avoid duplicate questions.
- Use clear student-friendly language.
- Cover different concepts when possible.

STUDY MATERIAL:

{notes}
"""

    try:

        response = ask_ollama(prompt)

        cleaned = clean_json_response(response)

        quiz_data = json.loads(cleaned)

        if not isinstance(quiz_data, list):
            return []

        valid_questions = []

        for question in quiz_data:

            validated = validate_question(question)

            if validated:
                valid_questions.append(validated)

        return valid_questions[:number]

    except Exception as error:

        print("Quiz generation error:", error)

        return []