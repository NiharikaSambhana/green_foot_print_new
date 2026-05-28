# backend/config.py

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

BASE_URL = os.getenv("BASE_URL", "https://genailab.tcs.in")

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "azure/genailab-maas-text-embedding-3-large"
)

CHAT_MODEL = os.getenv(
    "CHAT_MODEL",
    "azure_ai/genailab-maas-DeepSeek-V3-0324"
)

API_KEY = os.getenv("API_KEY")

DATA_FOLDER = BASE_DIR / "data"

VECTOR_DB = BASE_DIR / "vectordb" / "chroma_db"

CHUNK_SIZE = 1000

CHUNK_OVERLAP = 200

TOP_K_RESULTS = 4

MAX_CONTEXT_CHARS = 12000

ALLOW_INSECURE_SSL = True