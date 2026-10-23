import os
from openai import OpenAI

MODERATION_MODEL = "omni-moderation-latest"
DEFAULT_TIMEOUT = 30
DEFAULT_MAX_RETRIES = 2


def get_openai_client():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    return OpenAI(
        api_key=api_key,
        timeout=DEFAULT_TIMEOUT,
        max_retries=DEFAULT_MAX_RETRIES,
    )


def build_moderation_payload(text: str, model: str = MODERATION_MODEL) -> dict:
    return {
        "model": model,
        "input": text,
    }


def parse_moderation_response(response) -> dict:
    result = response.results[0]
    categories = dict(result.categories)
    category_scores = dict(result.category_scores)
    return {
        "flagged": result.flagged,
        "categories": categories,
        "category_scores": category_scores,
    }


def build_chat_payload(
    messages: list[dict], model: str = "gpt-4o", temperature: float = 0.0
) -> dict:
    return {
        "model": model,
        "messages": messages,
        "temperature": temperature,
    }


def build_embedding_payload(text: str, model: str = "text-embedding-3-small") -> dict:
    return {
        "model": model,
        "input": text,
    }


def build_tts_payload(text: str, model: str = "tts-1", voice: str = "alloy") -> dict:
    return {
        "model": model,
        "input": text,
        "voice": voice,
    }
