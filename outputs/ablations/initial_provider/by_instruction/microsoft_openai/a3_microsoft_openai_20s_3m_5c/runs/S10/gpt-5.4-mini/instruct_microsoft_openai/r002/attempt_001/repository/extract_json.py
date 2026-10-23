import json

from model_client import client, default_model, normalize_messages


def extract_json(text: str, model: str | None = None) -> dict:
    resp = client().responses.create(
        model=model or default_model(),
        input=normalize_messages(text, "Extract structured JSON only."),
        text={"format": {"type": "json_object"}},
    )
    return json.loads(resp.output_text)
