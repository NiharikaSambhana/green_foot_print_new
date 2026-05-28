# backend/test_rag.py

from chatbot import ask_question

question = (
    "What causes carbon emissions "
    "in large language models?"
)

print("\nTesting RAG Pipeline...\n")

print("Question:")
print(question)

answer = ask_question(question)

print("\nFinal Response:\n")

print(answer)