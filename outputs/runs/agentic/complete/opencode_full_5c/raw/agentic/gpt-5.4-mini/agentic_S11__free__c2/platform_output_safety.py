from openai import OpenAI

from model_client import build_platform_client, load_platform_config
from model_models import normalize_text


def platform_output_safety(text: str) -> bool:
    cfg = load_platform_config()
    client: OpenAI = build_platform_client(cfg)
    moderation = client.moderations.create(
        model="omni-moderation-latest", input=normalize_text(text)
    )
    return not moderation.results[0].flagged
