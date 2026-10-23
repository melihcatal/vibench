import os
from typing import Dict, Any, Optional
from pydantic import BaseSettings


class ModelClientConfig(BaseSettings):
    AZURE_AI_INFERENCE_ENDPOINT: Optional[str] = None
    AZURE_AI_INFERENCE_KEY: Optional[str] = None
    AZURE_AI_INFERENCE_DEPLOYMENT_NAME: Optional[str] = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


def get_model_client_config() -> Dict[str, Any]:
    """
    Loads and returns the Azure AI Inference configuration from environment variables.
    """
    config = ModelClientConfig()
    return {
        "AZURE_AI_INFERENCE_ENDPOINT": config.AZURE_AI_INFERENCE_ENDPOINT,
        "AZURE_AI_INFERENCE_KEY": config.AZURE_AI_INFERENCE_KEY,
        "AZURE_AI_INFERENCE_DEPLOYMENT_NAME": config.AZURE_AI_INFERENCE_DEPLOYMENT_NAME,
    }
