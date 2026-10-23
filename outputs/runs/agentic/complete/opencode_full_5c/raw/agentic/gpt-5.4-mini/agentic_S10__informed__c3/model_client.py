import os
from functools import lru_cache
from openai import OpenAI

_MODEL_FAMILY_MAP = {
    "summarization": os.getenv("OPENAI_SUMMARY_MODEL", "gpt-4.1-mini"),
    "json_extraction": os.getenv("OPENAI_JSON_MODEL", "gpt-4.1-mini"),
    "qa": os.getenv("OPENAI_QA_MODEL", "gpt-4.1"),
    "streaming": os.getenv("OPENAI_STREAM_MODEL", "gpt-4.1-mini"),
}


@lru_cache(maxsize=1)
def get_llm_client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def select_chat_model(task: str) -> str:
    return _MODEL_FAMILY_MAP.get(task, os.getenv("OPENAI_DEFAULT_MODEL", "gpt-4.1-mini"))
