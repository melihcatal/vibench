from openai import AzureOpenAI
from model_client import get_azure_openai_config


def select_platform_resource(model_hint: str) -> str:
    config = get_azure_openai_config()
    client = AzureOpenAI(**config)
    deployments = client.beta.deployments.list()
    for deployment in deployments.data:
        if model_hint.lower() in deployment.model.lower():
            return deployment.id
    raise ValueError(f"No deployment found matching '{model_hint}'")
