# backend/chatbot.py

import logging
import time
import httpx

from langchain_openai import ChatOpenAI

from config import (
    BASE_URL,
    API_KEY,
    CHAT_MODEL,
    ALLOW_INSECURE_SSL
)

from agents.guardrail_agent import (
    is_allowed_query,
    rejection_message
)

from agents.rag_agent import (
    retrieve_context,
    SYSTEM_PROMPT
)

from agents.summarizer_agent import (
    summarize_response
)

from agents.evaluator_agent import (
    evaluate_answer
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = httpx.Client(
    verify=not ALLOW_INSECURE_SSL
)

llm = ChatOpenAI(
    base_url=BASE_URL,
    api_key=API_KEY,
    model=CHAT_MODEL,
    temperature=0,
    timeout=30,
    http_client=client
)



def ask_question(question):

    if not question or not question.strip():

        return (
            "Please enter a valid sustainability question."
        )

    try:

        logger.info(
            f"Question Received: {question}"
        )

        # AGENT 1 - Guardrail

        if not is_allowed_query(question):

            logger.warning(
                "Query rejected by guardrails"
            )

            return rejection_message()

        # AGENT 2 - Retrieval

        context, sources = retrieve_context(question)

        if not context.strip():

            return (
                "Insufficient sustainability data available."
            )

        prompt = f"""
{SYSTEM_PROMPT}

Context:
<<<CONTEXT>>>
{context}
<<<END_CONTEXT>>>

Question:
<<<QUESTION>>>
{question}
<<<END_QUESTION>>>

Answer ONLY using the provided context.
"""

        # AGENT 3 - LLM Generation

        response = None

        for attempt in range(3):

            try:

                response = llm.invoke(prompt)

                break

            except Exception as e:

                logger.error(
                    f"Retry {attempt+1} failed: {e}"
                )

                time.sleep(2)

        if response is None:

            return "LLM generation failed."

        # AGENT 4 - Evaluation

        evaluation = evaluate_answer(
            question,
            context,
            response.content
        )

        # AGENT 5 - Summarization

        final_answer = summarize_response(
            response.content,
            evaluation,
            sources
        )

        return final_answer

    except Exception as e:

        logger.error(f"System Error: {e}")

        return f"System Error: {str(e)}"


if __name__ == "__main__":

    print("\n")
    print("=" * 50)
    print(" GreenPrompt Agentic AI ")
    print("=" * 50)

    print("\nType 'exit' to stop\n")

    while True:

        question = input("Ask Question: ")

        if question.lower() == "exit":

            print("\nGoodbye!")

            break

        answer = ask_question(question)

        print("\nBot Response:\n")

        print(answer)

        print("\n" + "=" * 50)