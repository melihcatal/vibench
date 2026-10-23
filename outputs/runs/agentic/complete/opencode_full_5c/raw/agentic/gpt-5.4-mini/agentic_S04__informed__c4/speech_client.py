import os
from typing import Any, Dict, Optional


def get_env(name: str, default: Optional[str] = None) -> str:
    value = os.getenv(name, default)
    if value is None:
        raise RuntimeError(f"Missing environment variable: {name}")
    return value


def assemblyai_headers() -> Dict[str, str]:
    return {
        "authorization": get_env("ASSEMBLYAI_API_KEY"),
        "content-type": "application/json",
    }


def assemblyai_base_url() -> str:
    return os.getenv("ASSEMBLYAI_BASE_URL", "https://api.assemblyai.com/v2")


def openai_client_kwargs() -> Dict[str, Any]:
    return {"api_key": get_env("OPENAI_API_KEY")}


def azure_translator_config() -> Dict[str, str]:
    return {
        "key": get_env("AZURE_TRANSLATOR_KEY"),
        "region": get_env("AZURE_TRANSLATOR_REGION"),
    }


def perspective_api_key() -> str:
    return get_env("PERSPECTIVE_API_KEY")
