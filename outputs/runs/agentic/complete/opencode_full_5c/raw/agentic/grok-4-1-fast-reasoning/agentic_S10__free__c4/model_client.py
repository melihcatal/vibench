import os
from openai import OpenAI
from typing import Optional


def get_llm_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")
    return OpenAI(api_key=api_key)


MODEL_FAMILY_TO_MODEL = {
    "gpt-4o-mini": "gpt-4o-mini",
    "gpt-4o": "gpt-4o",
    "gpt-3.5-turbo": "gpt-3.5-turbo",
    "text-embedding-3-small": "text-embedding-3-small",
    "tts-1": "tts-1",
}


def get_model_id(model_family: str) -> str:
    return MODEL_FAMILY_TO_MODEL.get(model_family, model_family)
