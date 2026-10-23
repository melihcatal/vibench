import json
from model_client import get_client
from model_models import build_messages, normalize_completion

def extract_json(text: str, schema: str) -> dict:
    client = get_client()
    system = f"You are a precise JSON extractor. Follow this schema exactly: {schema}. Output only valid JSON, no extra text."
    user = f"Extract from this text:\n\n{text}"
    messages = build_messages(system, user)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        response_format={"type": "json_object"},
        temperature=0.0
    )
    content = normalize_completion(response)
    return json.loads(content)