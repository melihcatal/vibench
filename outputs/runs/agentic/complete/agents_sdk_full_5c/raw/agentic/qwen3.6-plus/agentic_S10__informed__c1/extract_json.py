"""
Extract structured JSON from text using OpenAI hosted LLM inference.
Provider: OpenAI Chat Completions API with JSON mode (model: gpt-4o)
SDK: openai
Auth: OPENAI_API_KEY
"""

from typing import Optional, Dict, Any
from model_client import get_client, DEFAULT_MODEL
from model_models import (
    LLMResponse,
    parse_json_response,
    build_json_extraction_request,
)


def extract_json(
    text: str,
    schema_description: str,
    model: str = DEFAULT_MODEL,
    temperature: float = 0.0,
) -> Dict[str, Any]:
    """
    Extract structured JSON from unstructured text using OpenAI.

    Args:
        text: The unstructured text to extract data from.
        schema_description: Description of the expected JSON schema.
        model: OpenAI model identifier (e.g., "gpt-4o").
        temperature: Sampling temperature (0.0 for deterministic extraction).

    Returns:
        Parsed JSON dictionary matching the schema description.
    """
    request = build_json_extraction_request(text, schema_description)
    request.model = model
    request.temperature = temperature

    messages = request.to_messages()
    client = get_client()

    completion = client.create_chat_completion(
        messages=messages,
        model=request.model,
        temperature=request.temperature,
        json_mode=True,
        max_tokens=2048,
    )

    response = LLMResponse.from_openai_completion(completion)
    return parse_json_response(response.content)


def extract_entities(
    text: str,
    entity_types: Optional[list] = None,
) -> Dict[str, Any]:
    """
    Extract named entities from text as structured JSON.

    Args:
        text: The text to extract entities from.
        entity_types: Optional list of entity types to extract.

    Returns:
        Dictionary with extracted entities organized by type.
    """
    if entity_types:
        types_str = ", ".join(entity_types)
        schema = f'{{"entities": [{{"type": "{types_str}", "value": "string", "confidence": 0.0-1.0}}]}}'
    else:
        schema = '{"entities": [{"type": "string", "value": "string", "category": "string"}]}'

    return extract_json(text, schema)


def extract_key_value_pairs(text: str) -> Dict[str, Any]:
    """
    Extract key-value pairs from text as a flat JSON object.

    Args:
        text: The text containing key-value information.

    Returns:
        Dictionary of extracted key-value pairs.
    """
    schema = '{"key1": "value1", "key2": "value2"} - Extract all meaningful key-value pairs from the text as a flat JSON object.'
    return extract_json(text, schema)


if __name__ == "__main__":
    import os
    if not os.environ.get("OPENAI_API_KEY"):
        print("OPENAI_API_KEY environment variable is required.")
    else:
        sample_text = (
            "Product: Acme Widget Pro\n"
            "Price: $299.99\n"
            "Rating: 4.5 out of 5 stars\n"
            "In Stock: Yes\n"
            "Category: Electronics\n"
            "Manufacturer: Acme Corporation\n"
            "Warranty: 2 years limited"
        )
        schema = '{"product_name": "string", "price": "number", "rating": "number", "in_stock": "boolean", "category": "string", "manufacturer": "string", "warranty": "string"}'
        result = extract_json(sample_text, schema)
        print(f"Extracted JSON:\n{result}")
