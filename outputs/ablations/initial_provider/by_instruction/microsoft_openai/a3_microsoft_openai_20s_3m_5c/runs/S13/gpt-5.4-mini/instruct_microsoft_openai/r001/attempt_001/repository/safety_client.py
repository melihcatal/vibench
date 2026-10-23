import os
from typing import Any, Dict, Optional

from openai import OpenAI


DEFAULT_MODERATION_MODEL = "omni-moderation-latest"
DEFAULT_REASONING_MODEL = "gpt-5.4-mini"
DEFAULT_TRANSLATION_MODEL = "gpt-4.1-mini"
DEFAULT_TTS_MODEL = "gpt-4o-mini-tts"
DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"


def get_api_key() -> Optional[str]:
    return os.getenv("OPENAI_API_KEY")


def get_client() -> OpenAI:
    return OpenAI(api_key=get_api_key())


def get_model(name: Optional[str], default: str) -> str:
    return name or default


def extract_category_scores(result: Any) -> Dict[str, float]:
    scores = getattr(result, "category_scores", None) or {}
    return {str(k): float(v) for k, v in scores.items()}


def extract_categories(result: Any) -> Dict[str, bool]:
    categories = getattr(result, "categories", None) or {}
    return {str(k): bool(v) for k, v in categories.items()}
