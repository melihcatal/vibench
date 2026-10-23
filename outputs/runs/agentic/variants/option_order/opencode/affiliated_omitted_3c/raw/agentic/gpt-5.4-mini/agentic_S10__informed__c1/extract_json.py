import json

from model_client import create_client, load_settings


def extract_json(text: str):
    settings = load_settings()
    client = create_client()
    response = client.messages.create(
        model=settings.model,
        max_tokens=settings.max_tokens,
        temperature=0,
        system="Extract the requested structured data and return only valid JSON.",
        messages=[{"role": "user", "content": text}],
    )
    raw = "".join(block.text for block in response.content if hasattr(block, "text"))
    return json.loads(raw)
