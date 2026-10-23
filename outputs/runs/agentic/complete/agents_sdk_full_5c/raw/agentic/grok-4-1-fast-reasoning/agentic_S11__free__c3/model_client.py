import os
from openai import AzureOpenAI

def get_platform_client() -> AzureOpenAI:
    return AzureOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version="2024-02-15-preview"
    )

def get_platform_deployment(model_family: str) -> str:
    deployments = {
        "gpt-4o-mini": "gpt-4o-mini-deployment",
        "gpt-4o": "gpt-4o-deployment",
        "gpt-4-turbo": "gpt-4-turbo-deployment",
    }
    return deployments.get(model_family, "gpt-4o-mini-deployment")
