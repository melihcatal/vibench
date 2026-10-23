import os
from functools import lru_cache
from openai import OpenAI


@lru_cache(maxsize=1)
def get_client() -> OpenAI:
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def get_model_name(task: str) -> str:
    mapping = {
        "summary": os.environ.get("OPENAI_SUMMARY_MODEL", "gpt-4.1-mini"),
        "extract": os.environ.get("OPENAI_EXTRACT_MODEL", "gpt-4.1-mini"),
        "qa": os.environ.get("OPENAI_QA_MODEL", "gpt-4.1-mini"),
        "stream": os.environ.get("OPENAI_STREAM_MODEL", "gpt-4.1-mini"),
        "safety": os.environ.get("OPENAI_SAFETY_MODEL", "gpt-4.1-mini"),
        "translate": os.environ.get("OPENAI_TRANSLATE_MODEL", "gpt-4.1-mini"),
        "embed": os.environ.get("OPENAI_EMBED_MODEL", "text-embedding-3-large"),
        "spoken": os.environ.get("OPENAI_SPOKEN_MODEL", "gpt-4.1-mini"),
    }
    return mapping.get(task, os.environ.get("OPENAI_DEFAULT_MODEL", "gpt-4.1-mini"))
