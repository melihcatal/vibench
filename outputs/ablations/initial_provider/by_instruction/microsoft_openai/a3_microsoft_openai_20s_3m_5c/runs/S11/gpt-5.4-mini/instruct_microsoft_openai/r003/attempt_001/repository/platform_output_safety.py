from openai import AzureOpenAI

from model_client import build_platform_client, load_platform_config
from model_models import normalize_text


def platform_output_safety(text: str) -> bool:
    config = load_platform_config()
    client: AzureOpenAI = build_platform_client(config)
    result = client.moderations.create(input=normalize_text(text), model="omni-moderation-latest")
    return not any(getattr(item, "flagged", False) for item in result.results)
