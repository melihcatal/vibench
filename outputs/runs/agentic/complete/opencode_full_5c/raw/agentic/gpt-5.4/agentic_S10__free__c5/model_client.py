import os

from openai import OpenAI


def get_openai_client() -> OpenAI:
    api_key = os.environ["OPENAI_API_KEY"]
    base_url = os.environ.get("OPENAI_BASE_URL")
    if base_url:
        return OpenAI(api_key=api_key, base_url=base_url)
    return OpenAI(api_key=api_key)


def get_chat_model(task_name: str, default_model: str = "gpt-4.1-mini") -> str:
    env_key = f"OPENAI_{task_name.upper()}_MODEL"
    return os.environ.get(env_key, os.environ.get("OPENAI_MODEL", default_model))


def get_embedding_model() -> str:
    return os.environ.get("OPENAI_EMBEDDING_MODEL", "text-embedding-3-large")


def get_tts_model() -> str:
    return os.environ.get("OPENAI_TTS_MODEL", "gpt-4o-mini-tts")


def get_moderation_model() -> str:
    return os.environ.get("OPENAI_MODERATION_MODEL", "omni-moderation-latest")
