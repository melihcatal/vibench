from typing import Dict, Any, Optional
import os
import json
from dataclasses import dataclass


def get_model_client_config() -> Dict[str, Any]:
    """
    Loads Azure AI Inference configuration from environment variables.
    """
    config = {
        "AZURE_AI_INFERENCE_ENDPOINT": os.getenv("AZURE_AI_INFERENCE_ENDPOINT"),
        "AZURE_AI_INFERENCE_KEY": os.getenv("AZURE_AI_INFERENCE_KEY"),
        "AZURE_AI_INFERENCE_DEPLOYMENT_NAME": os.getenv(
            "AZURE_AI_INFERENCE_DEPLOYMENT_NAME"
        ),
        "AZURE_AI_INFERENCE_MODEL_ID": os.getenv(
            "AZURE_AI_INFERENCE_MODEL_ID", "gpt-4o"
        ),
    }
    return config


def normalize_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalizes request payload for Azure AI Inference.
    """
    normalized = {
        "messages": payload.get("messages", []),
        "system_message": payload.get("system_message", ""),
        "data_sources": payload.get("data_sources", None),
    }
    return normalized
