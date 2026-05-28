# backend/agents/retrieval_agent.py

import logging
import httpx

from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

from config import (
    BASE_URL,
    EMBEDDING_MODEL,
    API_KEY,
    VECTOR_DB,
    TOP_K_RESULTS,
    ALLOW_INSECURE_SSL
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = httpx.Client(
    verify=not ALLOW_INSECURE_SSL
)



def get_vector_db():

    embedding_model = OpenAIEmbeddings(
        base_url=BASE_URL,
        model=EMBEDDING_MODEL,
        api_key=API_KEY,
        http_client=client
    )

    vectordb = Chroma(
        persist_directory=str(VECTOR_DB),
        embedding_function=embedding_model
    )

    return vectordb



def retrieve_chunks(query, k=TOP_K_RESULTS):

    if not query or not query.strip():
        return []

    try:

        vectordb = get_vector_db()

        retriever = vectordb.as_retriever(
            search_type="mmr",
            search_kwargs={
                "k": k,
                "fetch_k": 10
            }
        )

        docs = retriever.invoke(query)

        logger.info(
            f"Retrieved {len(docs)} chunks"
        )

        return docs

    except Exception as e:

        logger.error(
            f"Retrieval failed: {e}"
        )

        return []