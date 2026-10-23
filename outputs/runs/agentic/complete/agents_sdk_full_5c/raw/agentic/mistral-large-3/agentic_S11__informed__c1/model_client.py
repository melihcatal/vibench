import os
from typing import Dict, Optional
import yaml


def load_config() -> Dict[str, str]:
    """Loads configuration from a local YAML file or environment variables."""
    config_path = os.getenv("MODEL_CONFIG_PATH", "model_config.yaml")
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            return yaml.safe_load(f)
    return {}


def get_azure_openai_config() -> Dict[str, str]:
    """Returns Azure OpenAI-specific configuration."""
    config = load_config().get("azure_openai", {})
    return {
        "deployment_name": os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", config.get("deployment_name")),
        "api_version": os.getenv("AZURE_OPENAI_API_VERSION", config.get("api_version", "2024-02-15-preview")),
        "model_identifier": os.getenv("AZURE_OPENAI_MODEL_IDENTIFIER", config.get("model_identifier", "gpt-4"))
    }