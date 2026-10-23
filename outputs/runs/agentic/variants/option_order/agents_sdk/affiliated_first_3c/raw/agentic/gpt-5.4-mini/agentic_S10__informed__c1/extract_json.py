from __future__ import annotations

from openai import OpenAI

from model_client import choose_model, get_openai_client, normalize_messages
from model_models import JsonExtraction, parse_json_object


def extract_json(text: str, schema_hint: str, model: str | None = None) -> JsonExtraction:
    client: OpenAI = get_openai_client()
    messages = normalize_messages(
        "Extract structured JSON only. Follow the schema hint exactly.",
        f"Text: {text}\n\nSchema hint: {schema_hint}",
    )
    response = client.chat.completions.create(
        model=choose_model(model, family="chat"),
        messages=messages,
        temperature=0.0,
        response_format={"type": "json_object"},
    )
    content = response.choices[0].message.content or "{}"
    return JsonExtraction(data=parse_json_object(content), model=choose_model(model, family="chat"))
