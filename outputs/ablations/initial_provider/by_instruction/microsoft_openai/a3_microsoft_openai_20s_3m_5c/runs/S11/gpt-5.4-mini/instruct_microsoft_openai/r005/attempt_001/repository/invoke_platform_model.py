import os
from openai import AzureOpenAI
from model_client import build_azure_openai_client, get_default_platform_model_name
from model_models import normalize_text_output


def invoke_platform_model(prompt: str, *, model: str | None = None, deployment: str | None = None) -> str:
    client: AzureOpenAI = build_azure_openai_client()
    target = deployment or model or get_default_platform_model_name()
    response = client.responses.create(model=target, input=prompt)
    return normalize_text_output(response)


if __name__ == "__main__":
    prompt = os.environ.get("PLATFORM_PROMPT", "Summarize the managed model workflow in one sentence.")
    print(invoke_platform_model(prompt))
