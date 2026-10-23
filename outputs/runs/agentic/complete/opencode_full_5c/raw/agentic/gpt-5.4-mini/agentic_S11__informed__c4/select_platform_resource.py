from openai import AzureOpenAI

from model_client import build_client, default_deployment


def select_platform_resource(preferred: str | None = None) -> str:
    client: AzureOpenAI = build_client()
    deployment = preferred or default_deployment()
    client.models.retrieve(deployment)
    return deployment
