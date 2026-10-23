import os
from openai import AzureOpenAI
from model_client import build_azure_openai_client, get_default_platform_model_name


def stream_platform_generation(prompt: str, *, model: str | None = None, deployment: str | None = None):
    client: AzureOpenAI = build_azure_openai_client()
    target = deployment or model or get_default_platform_model_name()
    stream = client.responses.create(model=target, input=prompt, stream=True)
    for event in stream:
        yield event


if __name__ == "__main__":
    prompt = os.environ.get("PLATFORM_PROMPT", "Stream a short briefing about managed model invocation.")
    for event in stream_platform_generation(prompt):
        print(event)
