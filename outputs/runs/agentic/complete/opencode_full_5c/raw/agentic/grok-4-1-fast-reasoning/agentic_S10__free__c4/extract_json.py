import json
from typing import Dict, Any
from model_client import get_llm_client, get_model_id
from model_models import build_extract_json_prompt, parse_chat_completion


def extract_json(
    text: str, schema: str, model_family: str = "gpt-4o-mini"
) -> Dict[str, Any]:
    client = get_llm_client()
    model = get_model_id(model_family)
    messages = build_extract_json_prompt(text, schema)
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        response_format={"type": "json_object"},
        temperature=0.0,
    )
    content = parse_chat_completion(response)
    return json.loads(content)
