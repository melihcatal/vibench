import os
from openai import AzureOpenAI
from model_client import build_azure_openai_client, get_default_platform_model_name
from model_models import collect_response_metadata


def collect_platform_metadata(prompt: str, *, model: str | None = None, deployment: str | None = None) -> dict:
    client: AzureOpenAI = build_azure_openai_client()
    target = deployment or model or get_default_platform_model_name()
    response = client.responses.create(model=target, input=prompt)
    return collect_response_metadata(response)


if __name__ == "__main__":
    prompt = os.environ.get("PLATFORM_PROMPT", "Return metadata for a managed model response.")
    print(collect_platform_metadata(prompt))
