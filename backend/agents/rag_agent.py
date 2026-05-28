# backend/agents/rag_agent.py

from agents.retrieval_agent import retrieve_chunks

from config import MAX_CONTEXT_CHARS

SYSTEM_PROMPT = """
You are GreenPrompt AI.

You are an enterprise sustainability expert.

Rules:

1. Answer ONLY using provided context.

2. Never hallucinate.

3. If information is unavailable say:

Insufficient sustainability data available.

4. Be concise and accurate.

5. Provide optimization recommendations.

6. Mention sources if available.
"""



def retrieve_context(question):

    docs = retrieve_chunks(question)

    if not docs:
        return "", []

    context = "\n\n".join([
        doc.page_content
        for doc in docs
    ])

    context = context[:MAX_CONTEXT_CHARS]

    sources = list(set([
        doc.metadata.get(
            "source_file",
            "unknown"
        )
        for doc in docs
    ]))

    return context, sources