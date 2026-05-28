# backend/agents/evaluator_agent.py

import json

from langchain_openai import ChatOpenAI

from config import (
    BASE_URL,
    API_KEY,
    CHAT_MODEL
)

judge = ChatOpenAI(
    base_url=BASE_URL,
    api_key=API_KEY,
    model=CHAT_MODEL,
    temperature=0,
    timeout=30,
    max_tokens=200
)



def evaluate_answer(
    question,
    context,
    answer
):

    prompt = f"""
You are an enterprise RAG evaluator.

Evaluate ONLY using the provided context.

Question:
<<<QUESTION>>>
{question}
<<<END>>>

Context:
<<<CONTEXT>>>
{context}
<<<END>>>

Answer:
<<<ANSWER>>>
{answer}
<<<END>>>

Return ONLY valid JSON:

{{
  "accuracy": 0,
  "relevance": 0,
  "groundedness": 0,
  "hallucination_detected": false,
  "feedback": "short feedback"
}}
"""

    try:

        result = judge.invoke(prompt)

        return json.loads(result.content)

    except Exception as e:

        return {
            "accuracy": 0,
            "relevance": 0,
            "groundedness": 0,
            "hallucination_detected": True,
            "feedback": str(e)
        }
