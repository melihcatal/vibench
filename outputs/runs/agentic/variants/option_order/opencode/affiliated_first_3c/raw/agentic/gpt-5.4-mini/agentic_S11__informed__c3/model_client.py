import os
from openai import AzureOpenAI
from model_models import PlatformRequest


def build_azure_openai_client() -> AzureOpenAI:
    return AzureOpenAI(
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-06-01"),
    )


def get_chat_model_name() -> str:
    return os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini")


def normalize_messages(request: PlatformRequest):
    if request.messages:
        return request.messages
    if request.prompt:
        return [{"role": "user", "content": request.prompt}]
    return [{"role": "user", "content": ""}]


def prompt_from_request(request: PlatformRequest) -> str:
    return request.prompt or ""
