from typing import Any
from model_models import (
    LLMRequest,
    LLMResponse,
    build_extraction_messages,
    parse_json_from_response,
)
from model_client import execute_chat


def extract_json(
    text: str,
    schema_description: str = "Extract all entities as a JSON object.",
    model: str = "mistral-large-latest",
) -> dict[str, Any]:
    messages = build_extraction_messages(text, schema_description=schema_description)
    request = LLMRequest(
        model=model,
        messages=messages,
        temperature=0.1,
        max_tokens=4096,
        top_p=0.9,
        response_format={"type": "json_object"},
    )
    response = execute_chat(request)
    return parse_json_from_response(response.content)
