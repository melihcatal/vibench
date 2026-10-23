import os
from openai import AzureOpenAI

DEPLOYMENTS = {
    "gpt-4o": "gpt-4o-deployment",
    "gpt-4o-mini": "gpt-4o-mini-deployment",
}

def get_platform_client():
    return AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version="2024-02-15-preview"
    )

def get_deployment(model_family: str = "gpt-4o-mini") -> str:
    return DEPLOYMENTS.get(model_family, "gpt-4o-mini-deployment")
