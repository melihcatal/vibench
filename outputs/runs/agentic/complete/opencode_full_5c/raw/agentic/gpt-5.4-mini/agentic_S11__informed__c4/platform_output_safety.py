from openai import AzureOpenAI

from model_client import build_client


def platform_output_safety(text: str) -> dict:
    client: AzureOpenAI = build_client()
    moderation = client.moderations.create(input=text)
    result = moderation.results[0] if moderation.results else None
    return {
        "flagged": bool(getattr(result, "flagged", False)),
        "categories": getattr(result, "categories", None),
        "raw": moderation,
    }
