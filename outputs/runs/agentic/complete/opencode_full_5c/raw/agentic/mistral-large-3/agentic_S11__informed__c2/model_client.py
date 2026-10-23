from typing import Dict, Any, Optional
import os
from dataclasses import dataclass
import yaml


@dataclass
class ModelClientConfig:
    default_model: str = "mistralai/Mistral-7B-Instruct-v0.1"
    default_max_tokens: int = 100
    default_temperature: float = 0.7
    api_timeout: int = 30


def get_model_client_config() -> ModelClientConfig:
    """
    Loads configuration for the Hugging Face Inference client.
    """
    config_path = os.getenv("MODEL_CLIENT_CONFIG_PATH", "model_client_config.yaml")

    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            config_data = yaml.safe_load(f)
        return ModelClientConfig(**config_data)

    return ModelClientConfig()
