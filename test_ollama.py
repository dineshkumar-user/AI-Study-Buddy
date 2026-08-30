from modules.ai_engine import ask_ollama


question = """
Explain inheritance in Python in simple words.
Give one simple example.
"""


answer = ask_ollama(question)

print("\n==============================")
print("AI RESPONSE")
print("==============================\n")

print(answer)