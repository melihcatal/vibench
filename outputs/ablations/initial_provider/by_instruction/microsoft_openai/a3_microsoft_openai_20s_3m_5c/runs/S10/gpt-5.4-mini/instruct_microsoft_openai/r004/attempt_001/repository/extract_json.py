from model_client import build_client, load_config
from model_models import json_prompt


def extract_json(text: str, provider: str = "openai") -> str:
    config = load_config(provider=provider)
    client = build_client(config)
    response = client.chat.completions.create(
        model=config.model,
        messages=[{"role": "user", "content": json_prompt(text)}],
        response_format={"type": "json_object"},
        temperature=0,
    )
    return response.choices[0].message.content or "{}"
