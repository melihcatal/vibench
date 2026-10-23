import json
from typing import Any
from model_client import chat_completion
from model_models import build_system_user_messages, parse_json_response


def extract_json(text: str, schema_description: str = "") -> dict[str, Any]:
    system_prompt = f"You extract structured information as JSON. Output ONLY valid JSON. Schema: {schema_description or 'arbitrary relevant fields'}"
    user_prompt = text
    messages = build_system_user_messages(system_prompt, user_prompt)
    response_format = {"type": "json_object"}
    content = chat_completion(messages, response_format=response_format)
    parsed = parse_json_response(content)
    return parsed if parsed else {}
