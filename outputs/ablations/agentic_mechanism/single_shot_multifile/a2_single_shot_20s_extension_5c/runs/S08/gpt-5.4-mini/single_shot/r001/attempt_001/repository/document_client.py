import os
from typing import Any, Dict, Optional
from openai import OpenAI

OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
OPENAI_BASE_URL_ENV = "OPENAI_BASE_URL"


def build_extract_client() -> OpenAI:
    api_key = os.getenv(OPENAI_API_KEY_ENV)
    base_url = os.getenv(OPENAI_BASE_URL_ENV)
    if base_url:
        return OpenAI(api_key=api_key, base_url=base_url)
    return OpenAI(api_key=api_key)


def coerce_text_input(document_text: Any) -> str:
    if document_text is None:
        return ""
    if isinstance(document_text, str):
        return document_text
    if isinstance(document_text, bytes):
        return document_text.decode("utf-8", errors="ignore")
    return str(document_text)


def load_provider_config() -> Dict[str, Optional[str]]:
    return {
        "api_key": os.getenv(OPENAI_API_KEY_ENV),
        "base_url": os.getenv(OPENAI_BASE_URL_ENV),
        "organization": os.getenv("OPENAI_ORG_ID"),
        "project": os.getenv("OPENAI_PROJECT_ID"),
    }
