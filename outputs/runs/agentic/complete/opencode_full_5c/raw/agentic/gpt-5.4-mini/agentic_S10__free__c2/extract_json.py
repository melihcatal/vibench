import json

from openai import OpenAI

from model_client import resolve_model


def extract_json(
    text: str, schema_hint: str | None = None, model: str | None = None
) -> dict:
    client = OpenAI()
    prompt = f"Extract structured JSON from this text. {schema_hint or ''}\n{text}"
    response = client.responses.create(model=resolve_model(model), input=prompt)
    return json.loads(response.output_text)
