import json
from typing import Any, Dict, Optional
from model_client import get_openai_client, select_text_model
from model_models import ChatPrompt, normalize_text_response


def extract_json(text: str, schema_hint: str, model: Optional[str] = None) -> Dict[str, Any]:
    client = get_openai_client()
    model_id = select_text_model(model=model, task="json_extraction")
    prompt = ChatPrompt(
        system="You extract structured data and return valid JSON only.",
        user=f"Extract the requested information as JSON. Schema hint: {schema_hint}\n\nText:\n{text}",
    )
    response = client.chat.completions.create(
        model=model_id,
        messages=prompt.to_messages(),
        temperature=0,
        response_format={"type": "json_object"},
    )
    content = normalize_text_response(response)
    return json.loads(content)
