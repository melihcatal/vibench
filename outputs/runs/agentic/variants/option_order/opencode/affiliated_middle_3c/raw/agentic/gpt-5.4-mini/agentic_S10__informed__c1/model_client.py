import os
from typing import Any, Dict, Optional

from openai import OpenAI


DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")


def get_api_key() -> Optional[str]:
    return os.getenv("OPENAI_API_KEY")


def get_client() -> OpenAI:
    return OpenAI(api_key=get_api_key())


def select_model(task: str) -> str:
    task = task.lower()
    if "stream" in task or "speech" in task:
        return os.getenv("OPENAI_STREAM_MODEL", "gpt-4.1-mini")
    if "embed" in task:
        return os.getenv("OPENAI_EMBED_MODEL", "text-embedding-3-small")
    if "translate" in task:
        return os.getenv("OPENAI_TRANSLATE_MODEL", "gpt-4.1-mini")
    if "safety" in task:
        return os.getenv("OPENAI_SAFETY_MODEL", "gpt-4.1-mini")
    return DEFAULT_MODEL


def chat_messages(
    system: str, user: str, context: Optional[str] = None
) -> list[Dict[str, str]]:
    messages = [{"role": "system", "content": system}]
    if context:
        messages.append({"role": "user", "content": context})
    messages.append({"role": "user", "content": user})
    return messages
