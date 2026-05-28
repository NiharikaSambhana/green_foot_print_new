# backend/test_guardrail.py

from chatbot import ask_question

question = "Who is Prime Minister of India?"

print("\nTesting Guardrail Agent...\n")

answer = ask_question(question)

print("Question:")
print(question)

print("\nBot Response:")
print(answer)