import os
from functools import lru_cache
from typing import Optional

from openai import OpenAI


def _env(name: str, default: Optional[str] = None) -> Optional[str]:
    value = os.getenv(name, default)
    return value if value else None


@lru_cache(maxsize=1)
def get_openai_client() -> OpenAI:
    return OpenAI(api_key=_env("OPENAI_API_KEY"))


def model_name(kind: str) -> str:
    mapping = {
        "summary": _env("OPENAI_SUMMARY_MODEL", "gpt-4.1-mini"),
        "extract": _env("OPENAI_EXTRACT_MODEL", "gpt-4.1-mini"),
        "qa": _env("OPENAI_QA_MODEL", "gpt-4.1"),
        "stream": _env("OPENAI_STREAM_MODEL", "gpt-4.1-mini"),
    }
    return mapping.get(kind, "gpt-4.1-mini")
