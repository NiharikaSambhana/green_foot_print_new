# backend/test_retriever.py

from agents.retrieval_agent import (
    retrieve_chunks
)

question = (
    "What is carbon emission?"
)

print("\nTesting Semantic Retrieval...\n")

results = retrieve_chunks(
    question,
    k=3
)

if not results:

    print("No retrieval results found.")

else:

    for idx, doc in enumerate(results, start=1):

        print(f"\nResult {idx}")

        print(
            f"Source: "
            f"{doc.metadata.get('source_file', 'unknown')}"
        )

        print(
            f"Chunk ID: "
            f"{doc.metadata.get('chunk_id', 'N/A')}"
        )

        print("\nContent:\n")

        print(doc.page_content[:500])

        print("\n" + "-" * 60)