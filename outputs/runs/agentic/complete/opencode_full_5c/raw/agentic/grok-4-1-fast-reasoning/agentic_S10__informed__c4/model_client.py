import os
from typing import Dict

PROVIDER_CONFIGS = {
    "anthropic": {
        "api_key_env": "ANTHROPIC_API_KEY",
        "default_model": "claude-3-haiku-20240307",
    },
    "openai": {"api_key_env": "OPENAI_API_KEY", "default_model": "gpt-4o-mini"},
    "google": {"api_key_env": "GOOGLE_API_KEY", "default_model": "gemini-1.5-flash"},
    "mistral": {"api_key_env": "MISTRAL_API_KEY", "default_model": "open-mistral-nemo"},
}


def get_api_key(provider: str) -> str:
    config = PROVIDER_CONFIGS[provider]
    key = os.getenv(config["api_key_env"])
    if not key:
        raise ValueError(f"API key for {provider} not set: {config['api_key_env']}")
    return key


def select_model_for_task(task: str) -> tuple[str, str]:
    task_models = {
        "summarize": ("anthropic", "claude-3-haiku-20240307"),
        "extract_json": ("openai", "gpt-4o-mini"),
        "answer_with_context": ("google", "gemini-1.5-flash"),
        "stream_completion": ("mistral", "open-mistral-nemo"),
    }
    return task_models.get(task, ("openai", "gpt-4o-mini"))
