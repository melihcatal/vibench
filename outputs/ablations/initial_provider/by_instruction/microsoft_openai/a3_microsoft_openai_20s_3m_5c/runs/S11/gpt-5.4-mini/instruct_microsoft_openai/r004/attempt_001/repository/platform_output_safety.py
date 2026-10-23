from openai import AzureOpenAI

from model_client import build_azure_openai_client


def platform_output_safety(text: str) -> bool:
    client = build_azure_openai_client()
    result = client.moderations.create(model="omni-moderation-latest", input=text)
    return not any(item.flagged for item in result.results)
