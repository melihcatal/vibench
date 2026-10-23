import json
from typing import Any, Dict
from model_client import get_client, MODEL_NAME
from model_models import make_messages, extract_content

def extract_json(text: str, schema_description: str) -> Dict[str, Any]:
    client = get_client()
    messages = make_messages(
        "You extract structured information from text. Respond ONLY with valid JSON object matching the schema. No extra text.",
        f"Schema description: {schema_description}\n\nText to extract from: {text}"
    )
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=0.0,
        response_format={"type": "json_object"},
        max_tokens=2000,
    )
    content = extract_content(response)
    return json.loads(content)
