from google.cloud import documentai_v1 as documentai
from google.cloud import translate_v3 as translate
from openai import OpenAI
import os
from typing import Optional, Dict, Any


def get_document_client(provider: str):
    """
    Returns a configured client for the specified OCR or document processing provider.

    Args:
        provider: The provider name (e.g., "google", "openai").

    Returns:
        Configured client for the provider.
    """
    if provider == "google":
        return documentai.DocumentProcessorServiceClient()
    elif provider == "google_translate":
        return translate.TranslationServiceClient()
    elif provider == "openai":
        return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    else:
        raise ValueError(f"Unsupported provider: {provider}")


def load_config(provider: str) -> Dict[str, Any]:
    """
    Loads configuration for the specified provider from environment variables.

    Args:
        provider: The provider name (e.g., "google", "azure").

    Returns:
        Dictionary containing provider-specific configuration.
    """
    config = {}

    if provider == "google":
        config.update(
            {
                "project_id": os.getenv("GOOGLE_CLOUD_PROJECT_ID"),
                "location": os.getenv("GOOGLE_DOCUMENT_AI_LOCATION", "us"),
                "processor_id": os.getenv("GOOGLE_DOCUMENT_AI_PROCESSOR_ID"),
            }
        )
    elif provider == "google_translate":
        config.update(
            {
                "project_id": os.getenv("GOOGLE_CLOUD_PROJECT_ID"),
                "location": os.getenv("GOOGLE_TRANSLATE_LOCATION", "global"),
            }
        )
    elif provider == "openai":
        config.update({"api_key": os.getenv("OPENAI_API_KEY")})
    elif provider == "azure":
        config.update(
            {
                "endpoint": os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"),
                "key": os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY"),
            }
        )

    return config
