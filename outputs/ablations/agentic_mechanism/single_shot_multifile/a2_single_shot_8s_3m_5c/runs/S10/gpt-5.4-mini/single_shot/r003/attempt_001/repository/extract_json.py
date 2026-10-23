from openai import OpenAI
from model_client import get_text_client, resolve_text_model
from model_models import normalize_json_result


def extract_json(text: str, schema_hint: str, model: str | None = None) -> dict:
    client = get_text_client()
    model_name = resolve_text_model(model, task="extract")
    prompt = f"Extract structured JSON from the text below. Follow this schema hint: {schema_hint}. Return only valid JSON.\n\n{text}"
    response = client.responses.create(model=model_name, input=prompt)
    return normalize_json_result(response)
