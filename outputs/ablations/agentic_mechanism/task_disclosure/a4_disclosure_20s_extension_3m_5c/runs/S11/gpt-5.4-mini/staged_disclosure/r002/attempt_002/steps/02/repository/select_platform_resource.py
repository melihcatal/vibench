import os
import requests


OPENAI_MODELS_ENDPOINT = "https://api.openai.com/v1/models"


def select_platform_resource(resource_name: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY is required")

    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get(OPENAI_MODELS_ENDPOINT, headers=headers, timeout=30)
    response.raise_for_status()
    data = response.json()
    models = data.get("data", [])

    if not resource_name:
        raise ValueError("resource_name is required")

    normalized = resource_name.strip()
    if not normalized:
        raise ValueError("resource_name is required")

    available = {item.get("id") for item in models if isinstance(item, dict)}
    if normalized in available:
        return normalized

    aliases = {
        "gpt-5.4-mini": "openai/gpt-5.4-mini",
        "gpt-4.1": "gpt-4.1",
        "gpt-4o": "gpt-4o",
    }
    resolved = aliases.get(normalized, normalized)
    if resolved in available:
        return resolved

    raise LookupError(f"OpenAI resource not available: {resource_name}")
