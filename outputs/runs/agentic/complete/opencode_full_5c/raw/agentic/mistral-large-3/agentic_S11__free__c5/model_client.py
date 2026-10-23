from typing import Dict, Any, Optional
import os
from pydantic import BaseModel


def get_model_client_config() -> Dict[str, str]:
    """
    Loads Azure AI Inference configuration from environment variables.
    """
    return {
        "AZURE_AI_INFERENCE_ENDPOINT": os.getenv("AZURE_AI_INFERENCE_ENDPOINT"),
        "AZURE_AI_INFERENCE_KEY": os.getenv("AZURE_AI_INFERENCE_KEY"),
        "AZURE_AI_INFERENCE_DEPLOYMENT": os.getenv(
            "AZURE_AI_INFERENCE_DEPLOYMENT", "gpt-4o"
        ),
    }


def normalize_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalizes request payload for Azure AI Inference.
    """
    normalized = {
        "messages": payload.get("messages", []),
        "temperature": payload.get("temperature", 1.0),
        "max_tokens": payload.get("max_tokens", 1000),
    }
    if "system_prompt" in payload:
        normalized["messages"].insert(
            0, {"role": "system", "content": payload["system_prompt"]}
        )
    return normalized
