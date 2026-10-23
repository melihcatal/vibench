import os
from dataclasses import dataclass, field
from typing import Any

from openai import OpenAI


DEFAULT_MODEL = "gpt-4o"
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 2048


@dataclass
class LLMConfig:
    api_key: str = field(default_factory=lambda: os.environ["OPENAI_API_KEY"])
    model: str = DEFAULT_MODEL
    temperature: float = DEFAULT_TEMPERATURE
    max_tokens: int = DEFAULT_MAX_TOKENS
    top_p: float = 1.0


def get_client(config: LLMConfig | None = None) -> OpenAI:
    if config is None:
        config = LLMConfig()
    return OpenAI(api_key=config.api_key)


def build_messages(
    system_prompt: str,
    user_prompt: str,
    history: list[dict[str, str]] | None = None,
) -> list[dict[str, str]]:
    messages: list[dict[str, str]] = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    if history:
        messages[1:1] = history
    return messages


def normalize_chat_response(response: Any) -> str:
    return response.choices[0].message.content.strip()


def get_model_family(model_id: str) -> str:
    families = {
        "gpt-4o": "gpt-4o",
        "gpt-4o-mini": "gpt-4o-mini",
        "gpt-4-turbo": "gpt-4",
        "gpt-3.5-turbo": "gpt-3.5",
        "o1": "o1",
        "o1-mini": "o1-mini",
    }
    for prefix, family in families.items():
        if model_id.startswith(prefix):
            return family
    return "unknown"
