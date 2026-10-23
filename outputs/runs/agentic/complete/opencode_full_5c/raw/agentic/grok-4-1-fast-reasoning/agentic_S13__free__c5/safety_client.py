import os

# Text Content Safety configuration
SAFETY_CONFIG = {
    "openai_api_key": os.getenv("OPENAI_API_KEY"),
    "perspective_api_key": os.getenv("PERSPECTIVE_API_KEY"),
    "azure_endpoint": os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT"),
    "azure_key": os.getenv("AZURE_CONTENT_SAFETY_KEY"),
    "huggingface_token": os.getenv("HUGGINGFACE_TOKEN"),
    "default_thresholds": {
        "toxicity": 0.5,
        "hate": 0.67,
        "harassment": 0.67,
        "self_harm": 0.5,
        "sexual": 0.8,
        "violence": 0.8,
    },
}


def check_config(provider: str) -> bool:
    key = f"{provider}_api_key" if provider != "azure" else f"{provider}_key"
    return bool(os.getenv(key.upper().replace("_", "_")))
