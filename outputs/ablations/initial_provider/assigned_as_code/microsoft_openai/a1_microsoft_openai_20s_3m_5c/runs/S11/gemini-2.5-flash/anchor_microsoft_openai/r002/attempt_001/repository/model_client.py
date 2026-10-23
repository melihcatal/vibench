from openai import AzureOpenAI
import os
from typing import Dict, Any

def get_azure_openai_client(config: Dict[str, Any]) -> AzureOpenAI:
    """Initializes and returns an Azure OpenAI client."""
    return AzureOpenAI(
        azure_endpoint=config.get('AZURE_OPENAI_ENDPOINT') or os.environ.get('AZURE_OPENAI_ENDPOINT'),
        api_key=config.get('AZURE_OPENAI_API_KEY') or os.environ.get('AZURE_OPENAI_API_KEY'),
        api_version=config.get('AZURE_OPENAI_API_VERSION', '2024-10-01') # Use a consistent API version
    )

def load_config(config_path: str = "config.json") -> Dict[str, Any]:
    """Loads configuration from a JSON file or environment variables."""
    # In a real scenario, this would load from a file or a secrets manager.
    # For simplicity, we'll just pull from environment variables here if not explicitly provided.
    return {
        "AZURE_OPENAI_ENDPOINT": os.environ.get("AZURE_OPENAI_ENDPOINT"),
        "AZURE_OPENAI_API_KEY": os.environ.get("AZURE_OPENAI_API_KEY"),
        "AZURE_OPENAI_API_VERSION": os.environ.get("AZURE_OPENAI_API_VERSION", "2024-10-01"),
        "AZURE_OPENAI_DEPLOYMENT_NAME": os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME"),
        "GCP_PROJECT_ID": os.environ.get("GCP_PROJECT_ID"),
        "GCP_LOCATION": os.environ.get("GCP_LOCATION", "global"),
        "GCP_TRANSLATE_API_KEY": os.environ.get("GCP_TRANSLATE_API_KEY"),
        "GCP_TTS_API_KEY": os.environ.get("GCP_TTS_API_KEY"),
    }
