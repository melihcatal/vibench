from openai import OpenAI

from model_client import build_client, load_config


def check_platform_output_safety(text: str) -> bool:
    config = load_config()
    client: OpenAI = build_client(config)
    moderation = client.moderations.create(
        model="omni-moderation-latest",
        input=text,
    )
    return not any(result.flagged for result in moderation.results)
