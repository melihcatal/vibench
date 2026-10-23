"""
Calls a hosted LLM (OpenAI GPT-4o) to extract structured JSON from text.

Provider: OpenAI (api.openai.com)
Model family: gpt-4o
"""

import json
from typing import Optional

from model_client import (
    get_sync_client,
    select_model_family,
    build_system_message,
    build_user_message,
    configure_completion_kwargs,
)
from model_models import (
    ExtractRequest,
    ExtractResponse,
    normalize_extracted_json,
    extract_text_from_openai_response,
    extract_token_usage,
)

OPENAI_API_HOST = "api.openai.com"
OPENAI_MODEL_FAMILY = "gpt-4o"


def build_extraction_instruction(request: ExtractRequest) -> str:
    """Build the system instruction for JSON extraction."""
    schema_desc = json.dumps(request.schema_hint, indent=2) if request.schema_hint else "a JSON object"
    strict_note = "You must return ONLY valid JSON, no other text." if request.strict else ""
    return (
        f"You are a structured data extraction assistant powered by OpenAI's {OPENAI_MODEL_FAMILY}. "
        f"Extract the requested data from the user's text and return it as valid JSON "
        f"matching this schema: {schema_desc}. "
        f"{strict_note}"
    )


def extract_json(
    request: ExtractRequest,
    model: Optional[str] = None,
    temperature: float = 0.0,
) -> ExtractResponse:
    """
    Extract structured JSON from text using OpenAI GPT-4o hosted LLM.

    Args:
        request: ExtractRequest with text and optional schema hint.
        model: Optional explicit OpenAI model identifier.
        temperature: Sampling temperature (default 0.0 for deterministic extraction).

    Returns:
        ExtractResponse containing parsed JSON and metadata.
    """
    selected_model = model or select_model_family("extract")

    system_msg = build_system_message(build_extraction_instruction(request))
    user_msg = build_user_message(request.text)

    client = get_sync_client()

    response_format = {"type": "json_object"} if request.strict else None

    kwargs = configure_completion_kwargs(
        messages=[system_msg, user_msg],
        model=selected_model,
        temperature=temperature,
        max_tokens=2048,
        response_format=response_format,
    )

    completion = client.chat.completions.create(**kwargs)

    raw_text = extract_text_from_openai_response(completion)
    usage = extract_token_usage(completion)

    try:
        parsed = normalize_extracted_json(raw_text, request.schema_hint if request.schema_hint else None)
    except (json.JSONDecodeError, ValueError):
        parsed = {"error": "Failed to parse JSON", "raw_output": raw_text}

    return ExtractResponse(
        extracted=parsed,
        raw_text=raw_text,
        model_used=selected_model,
        token_usage=usage,
    )


if __name__ == "__main__":
    sample = ExtractRequest(
        text="Extract entities from this: John Smith, age 45, works at Acme Corp as a senior engineer.",
        schema_hint={"name": "string", "age": "integer", "company": "string", "role": "string"},
        strict=True,
    )
    result = extract_json(sample)
    print(f"Model: {result.model_used}")
    print(f"Extracted: {json.dumps(result.extracted, indent=2)}")
