import os
from functools import lru_cache

from openai import OpenAI


def _getenv(name: str, default: str = "") -> str:
    return os.getenv(name, default)


@lru_cache(maxsize=1)
def get_client() -> OpenAI:
    return OpenAI(api_key=_getenv("OPENAI_API_KEY"))


def get_text_model() -> str:
    return _getenv("OPENAI_TEXT_MODEL", "gpt-4.1-mini")


def get_embedding_model() -> str:
    return _getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def pick_model(task: str) -> str:
    task = task.lower()
    if task in {
        "summarize",
        "extract_json",
        "answer",
        "safety",
        "translate",
        "spoken_brief",
    }:
        return get_text_model()
    if task == "embed":
        return get_embedding_model()
    return get_text_model()
