"""
Extract structured JSON from text using Anthropic Messages API with Claude model.
Provider: Anthropic (anthropic SDK, ANTHROPIC_API_KEY)
"""

import json
from typing import Optional, Dict, Any, List

import anthropic

from model_client import get_anthropic_client, normalize_completion_response
from model_models import LLMRequest, LLMResponse, ExtractedJSON


DEFAULT_JSON_MODEL = "claude-3-5-sonnet-20241022"


def extract_json_from_text(
    text: str,
    schema_description: Optional[str] = None,
    fields: Optional[List[str]] = None,
    model_id: Optional[str] = None,
    temperature: float = 0.2,
) -> ExtractedJSON:
    """
    Extract structured JSON from arbitrary text using Anthropic Claude.

    Args:
        text: Input text to extract JSON from.
        schema_description: Description of the expected JSON structure.
        fields: List of field names to extract.
        model_id: Anthropic model identifier.
        temperature: Low temperature for deterministic extraction.

    Returns:
        ExtractedJSON with parsed data or error info.
    """
    if model_id is None:
        model_id = DEFAULT_JSON_MODEL

    schema_part = ""
    if schema_description:
        schema_part = f"\nExpected JSON schema: {schema_description}"
    elif fields:
        schema_part = f"\nExtract only these fields as JSON keys: {', '.join(fields)}"

    system_prompt = (
        "You are a JSON extraction assistant. "
        "Analyze the input text and extract the requested information as valid JSON. "
        "Return ONLY the JSON object, wrapped in ```json code fences."
    )

    user_prompt = (
        f"Extract structured JSON from the following text.{schema_part}\n\n"
        f"---\n{text}\n---"
    )

    request = LLMRequest(
        text=user_prompt,
        system_prompt=system_prompt,
        model_id=model_id,
        max_tokens=4096,
        temperature=temperature,
    )

    client = get_anthropic_client()

    api_request = request.to_anthropic_messages()
    response = client.messages.create(**api_request)

    normalized = normalize_completion_response(response)

    return ExtractedJSON.from_text(normalized["text"])


def extract_json_with_schema(
    text: str,
    schema: Dict[str, Any],
    model_id: str = DEFAULT_JSON_MODEL,
) -> ExtractedJSON:
    """
    Extract JSON matching a specific schema from text.

    Args:
        text: Input text.
        schema: JSON schema describing the expected output structure.
        model_id: Anthropic model identifier.

    Returns:
        ExtractedJSON with parsed data.
    """
    schema_str = json.dumps(schema, indent=2)
    return extract_json_from_text(
        text,
        schema_description=f"Match this schema:\n{schema_str}",
        model_id=model_id,
    )
