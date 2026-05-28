# backend/ingest.py

import logging
from pathlib import Path
import shutil
import httpx

from langchain_community.document_loaders import (
    TextLoader,
    CSVLoader
)

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from langchain_chroma import Chroma

from langchain_openai import OpenAIEmbeddings

from config import (
    BASE_URL,
    EMBEDDING_MODEL,
    API_KEY,
    DATA_FOLDER,
    VECTOR_DB,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    ALLOW_INSECURE_SSL
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = httpx.Client(
    verify=not ALLOW_INSECURE_SSL
)


def load_documents():

    documents = []

    data_path = Path(DATA_FOLDER)

    if not data_path.exists():
        raise FileNotFoundError(
            f"Data folder not found: {DATA_FOLDER}"
        )

    for file in data_path.iterdir():

        try:

            if file.suffix.lower() in [".txt", ".log"]:

                loader = TextLoader(
                    str(file),
                    encoding="utf-8"
                )

                documents.extend(loader.load())

            elif file.suffix.lower() == ".csv":

                loader = CSVLoader(str(file))

                documents.extend(loader.load())

        except Exception as e:

            logger.error(
                f"Failed loading {file.name}: {e}"
            )

    return documents



def enrich_metadata(chunks):

    for idx, chunk in enumerate(chunks):

        chunk.metadata["chunk_id"] = idx

        chunk.metadata["source_file"] = (
            chunk.metadata.get(
                "source",
                "unknown"
            )
        )

        chunk.metadata["document_type"] = (
            Path(
                chunk.metadata[
                    "source_file"
                ]
            ).suffix
        )

        chunk.metadata["chunk_length"] = (
            len(chunk.page_content)
        )

    return chunks



def create_embedding_model():

    return OpenAIEmbeddings(
        base_url=BASE_URL,
        model=EMBEDDING_MODEL,
        api_key=API_KEY,
        http_client=client
    )



def build_vector_db():

    logger.info("Loading documents...")

    documents = load_documents()

    if not documents:
        raise ValueError(
            "No valid documents found"
        )

    logger.info(
        f"Documents Loaded: {len(documents)}"
    )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    chunks = splitter.split_documents(documents)

    logger.info(
        f"Chunks Created: {len(chunks)}"
    )

    chunks = enrich_metadata(chunks)

    embedding_model = create_embedding_model()

    vector_db_path = Path(VECTOR_DB)

    if vector_db_path.exists():
        shutil.rmtree(vector_db_path)

    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=str(VECTOR_DB)
    )

    logger.info("Vector Database Created Successfully")

    return vectordb


if __name__ == "__main__":

    build_vector_db()