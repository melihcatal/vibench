import os
from typing import Literal, TypedDict

DeepLAuth = str  # Placeholder for DeepL auth token

TranslationResult = TypedDict(
    "TranslationResult",
    {
        "translatedText": str,
    },
)

ModelConfig = TypedDict(
    "ModelConfig",
    {
        "service": Literal["DeepL", "Google", "Azure", "Amazon", "Alibaba"],
        "auth": DeepLAuth,
    },
)


def get_model_config() -> ModelConfig:
    """Return a configuration dict identifying the concrete provider to use."""
    return {"service": "DeepL", "auth": os.getenv("DEEPL_AUTH_KEY")}
