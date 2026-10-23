import os
from openai import AzureOpenAI
from model_models import PlatformResource


DEFAULT_CHAT_MODEL_FAMILY = "gpt-4o-mini"


def get_azure_openai_client() -> AzureOpenAI:
    endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
    api_key = os.environ["AZURE_OPENAI_API_KEY"]
    api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-21")
    return AzureOpenAI(
        azure_endpoint=endpoint, api_key=api_key, api_version=api_version
    )


def get_default_platform_resource() -> PlatformResource:
    deployment = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT", DEFAULT_CHAT_MODEL_FAMILY)
    model_family = os.getenv("AZURE_OPENAI_MODEL_FAMILY", DEFAULT_CHAT_MODEL_FAMILY)
    return PlatformResource(
        deployment_name=deployment,
        azure_deployment=deployment,
        model_family=model_family,
    )
