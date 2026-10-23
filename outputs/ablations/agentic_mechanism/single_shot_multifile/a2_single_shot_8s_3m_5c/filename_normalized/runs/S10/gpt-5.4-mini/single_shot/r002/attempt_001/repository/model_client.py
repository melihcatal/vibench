import os
from functools import lru_cache
from openai import OpenAI


_MODEL_DEFAULTS = {
    "summarization": os.getenv("OPENAI_SUMMARY_MODEL", "gpt-4.1-mini"),
    "extraction": os.getenv("OPENAI_EXTRACTION_MODEL", "gpt-4.1-mini"),
    "qa": os.getenv("OPENAI_QA_MODEL", "gpt-4.1-mini"),
    "streaming": os.getenv("OPENAI_STREAM_MODEL", "gpt-4.1-mini"),
    "safety": os.getenv("OPENAI_SAFETY_MODEL", "gpt-4.1-mini"),
    "translation": os.getenv("OPENAI_TRANSLATION_MODEL", "gpt-4.1-mini"),
    "embedding": os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"),
    "speech": os.getenv("OPENAI_SPEECH_MODEL", "gpt-4.1-mini"),
}


@lru_cache(maxsize=1)
def get_client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_model_name(task: str) -> str:
    return _MODEL_DEFAULTS.get(task, os.getenv("OPENAI_DEFAULT_MODEL", "gpt-4.1-mini"))
