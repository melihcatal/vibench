import os
from typing import Dict, Any


def get_azure_openai_config() -> Dict[str, str]:
    return {
        "api_key": os.getenv("AZURE_OPENAI_API_KEY"),
        "azure_endpoint": os.getenv("AZURE_OPENAI_ENDPOINT"),
        "api_version": "2024-02-15-preview",
    }


def get_openai_config() -> Dict[str, str]:
    return {"api_key": os.getenv("OPENAI_API_KEY")}
