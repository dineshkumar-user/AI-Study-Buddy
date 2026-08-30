import json
import re
from modules.ai_engine import ask_ollama


def clean_json_response(response):

    response = response.strip()

    response = re.sub(
        r"```json",
        "",
        response,
        flags=re.IGNORECASE
    )

    response = re.sub(
        r"```",
        "",
        response
    )

    response = response.strip()

    start = response.find("[")

    end = response.rfind("]")

    if start != -1 and end != -1:

        response = response[start:end + 1]

    return response


def generate_flashcards(notes, number=5):

    if not notes or not notes.strip():
        return []

    prompt = f"""
You are an AI flashcard generator.

Create exactly {number} useful educational flashcards
from the study material.

Return ONLY valid JSON.

Do not write markdown.
Do not add any text before or after the JSON.

Use exactly this format:

[
  {{
    "question": "Question about the concept",
    "answer": "Clear answer",
    "concept": "Concept name"
  }}
]

Rules:
- Questions must be based ONLY on the study material.
- Answers should be short and easy to understand.
- Avoid duplicate flashcards.
- Cover different concepts.
- Make the flashcards useful for revision.

STUDY MATERIAL:

{notes}
"""

    try:

        response = ask_ollama(prompt)

        cleaned = clean_json_response(response)

        cards = json.loads(cleaned)

        if not isinstance(cards, list):
            return []

        valid_cards = []

        for card in cards:

            if not isinstance(card, dict):
                continue

            if not all(
                key in card
                for key in [
                    "question",
                    "answer",
                    "concept"
                ]
            ):
                continue

            valid_cards.append({
                "question": str(
                    card["question"]
                ).strip(),

                "answer": str(
                    card["answer"]
                ).strip(),

                "concept": str(
                    card["concept"]
                ).strip()
            })

        return valid_cards[:number]

    except Exception as error:

        print("Flashcard generation error:", error)

        return []