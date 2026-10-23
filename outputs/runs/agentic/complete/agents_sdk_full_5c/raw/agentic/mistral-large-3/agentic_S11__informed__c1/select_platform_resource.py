import os
from typing import Dict, Optional
from openai import AzureOpenAI
from model_client import get_azure_openai_config


def resolve_model_deployment() -> Dict[str, str]:
    """
    Resolves the Azure OpenAI deployment name and model identifier for the current project.
    """
    config = get_azure_openai_config()
    client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=config["api_version"],
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
    )

    deployment_name = config["deployment_name"]
    model_identifier = config.get("model_identifier", "gpt-4")

    return {
        "deployment_name": deployment_name,
        "model_identifier": model_identifier,
        "api_version": config["api_version"]
    }