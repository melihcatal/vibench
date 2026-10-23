import os
from typing import Optional, Dict, Any
from openai import AzureOpenAI


def get_azure_openai_client() -> AzureOpenAI:
    """
    Initializes and returns an Azure OpenAI client using environment variables.
    """
    return AzureOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version="2024-02-01",
    )


def load_config() -> Dict[str, Any]:
    """
    Loads configuration for the managed model platform workflow.
    """
    return {
        "azure_openai": {
            "endpoint": os.getenv("AZURE_OPENAI_ENDPOINT"),
            "api_key": os.getenv("AZURE_OPENAI_API_KEY"),
            "deployment_name": os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            "api_version": "2024-02-01",
        }
    }
