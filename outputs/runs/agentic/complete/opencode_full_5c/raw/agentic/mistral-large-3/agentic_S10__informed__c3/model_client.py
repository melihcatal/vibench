import os
from typing import Dict, Any, Optional
from pydantic import BaseSettings


class ModelConfig(BaseSettings):
    summarization_model: str = "mistral-large-latest"
    extraction_model: str = "mistral-large-latest"
    qa_model: str = "mistral-large-latest"
    streaming_model: str = "mistral-large-latest"
    mistral_api_key: Optional[str] = os.getenv("MISTRAL_API_KEY")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


def get_model_config() -> Dict[str, Any]:
    config = ModelConfig()
    return {
        "summarization_model": config.summarization_model,
        "extraction_model": config.extraction_model,
        "qa_model": config.qa_model,
        "streaming_model": config.streaming_model,
    }
