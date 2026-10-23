import os
from typing import Any, Dict


def get_env(name: str, default: str = "") -> str:
    return os.getenv(name, default)


def provider_config() -> Dict[str, str]:
    return {
        "assemblyai_api_key": get_env("ASSEMBLYAI_API_KEY"),
        "assemblyai_base_url": get_env(
            "ASSEMBLYAI_BASE_URL", "https://api.assemblyai.com"
        ),
        "deepl_auth_key": get_env("DEEPL_AUTH_KEY"),
        "perspective_api_key": get_env("PERSPECTIVE_API_KEY"),
        "mistral_api_key": get_env("MISTRAL_API_KEY"),
        "cohere_api_key": get_env("COHERE_API_KEY"),
    }


def assemblyai_headers() -> Dict[str, str]:
    key = get_env("ASSEMBLYAI_API_KEY")
    return (
        {"authorization": key, "content-type": "application/json"}
        if key
        else {"content-type": "application/json"}
    )


def as_text(value: Any) -> str:
    return "" if value is None else str(value)
