import json
from model_client import get_llm_client
from model_models import (
    MODEL_FAMILY,
    create_system_message,
    create_user_message,
    normalize_response,
    DEFAULT_PARAMS,
)


def extract_json(text: str, schema_description: str = "") -> dict:
    client = get_llm_client()
    system_content = "You are a precise JSON extractor. Respond ONLY with a valid JSON object. No explanations or extra text."
    if schema_description:
        system_content += f" Match this schema: {schema_description}"
    messages = [create_system_message(system_content), create_user_message(text)]
    response = client.chat(
        model=MODEL_FAMILY, messages=messages, temperature=0.1, **DEFAULT_PARAMS
    )
    content = normalize_response(response)
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {}
