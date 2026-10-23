import os
from openai import AzureOpenAI
from model_client import build_azure_openai_client


def platform_output_safety(text: str) -> dict:
    client: AzureOpenAI = build_azure_openai_client()
    response = client.moderations.create(input=text)
    return response.model_dump() if hasattr(response, "model_dump") else dict(response)


if __name__ == "__main__":
    text = os.environ.get("PLATFORM_TEXT", "")
    print(platform_output_safety(text))
