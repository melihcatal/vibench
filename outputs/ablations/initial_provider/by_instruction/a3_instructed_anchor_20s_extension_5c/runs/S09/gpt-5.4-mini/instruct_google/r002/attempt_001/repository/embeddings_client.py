import os
from functools import lru_cache

import google.generativeai as genai


def api_key() -> str:
    key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not key:
        raise RuntimeError("Missing GOOGLE_API_KEY or GEMINI_API_KEY")
    return key


@lru_cache(maxsize=1)
def configure_client() -> None:
    genai.configure(api_key=api_key())


def embedding_model() -> str:
    return os.getenv("GOOGLE_EMBEDDING_MODEL", "models/text-embedding-004")


def task_type() -> str:
    return os.getenv("GOOGLE_EMBEDDING_TASK_TYPE", "retrieval_document")
