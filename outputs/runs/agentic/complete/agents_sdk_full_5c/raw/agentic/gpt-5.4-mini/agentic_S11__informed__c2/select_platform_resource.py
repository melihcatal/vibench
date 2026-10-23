from __future__ import annotations

from openai import AzureOpenAI

from model_client import get_client, get_deployment
from model_models import PlatformResource


def select_platform_resource() -> PlatformResource:
    client: AzureOpenAI = get_client()
    deployment = get_deployment()
    client.models.list()
    return PlatformResource(kind="deployment", identifier=deployment, provider="azure-openai")


if __name__ == "__main__":
    resource = select_platform_resource()
    print(resource.identifier)
