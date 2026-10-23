"""
Call a hosted LLM (OpenAI gpt-4o) to extract structured JSON from text.

Uses OpenAI platform API at api.openai.com with concrete model gpt-4o
and json_object response format.
"""

import json
from typing import Any, Dict, Optional

from model_client import create_openai_client, execute_chat_completion
from model_models import LLMRequest, build_system_prompt, build_completion_prompt


def extract_json(
    text: str,
    schema_description: str = "a JSON object with relevant extracted fields",
    model: str = "gpt-4o",
    temperature: float = 0.0,
) -> Dict[str, Any]:
    """Extract structured JSON from unstructured text using OpenAI's hosted LLM.

    Args:
        text: The source text to extract data from.
        schema_description: Description of the expected JSON structure.
        model: OpenAI model identifier (defaults to gpt-4o).
        temperature: Sampling temperature (0.0 recommended for extraction).

    Returns:
        Parsed JSON dict with extracted data.
    """
    system_prompt = build_system_prompt("extract_json", schema_description=schema_description)
    user_prompt = build_completion_prompt("extract_json", text=text)

    request = LLMRequest(
        model=model,
        prompt=user_prompt,
        system_prompt=system_prompt,
        temperature=temperature,
        max_tokens=2048,
        response_format={"type": "json_object"},
    )

    response = execute_chat_completion(request)
    result_text = response.text.strip()

    # Remove markdown fences if present
    if result_text.startswith("```"):
        lines = result_text.split("\n")
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
        result_text = "\n".join(lines).strip()

    return json.loads(result_text)


def extract_entities(
    text: str,
    entity_types: Optional[list] = None,
    model: str = "gpt-4o",
) -> Dict[str, Any]:
    """Extract named entities as JSON using OpenAI gpt-4o.

    Args:
        text: Source text.
        entity_types: List of entity types to extract (e.g., ['person', 'organization']).
        model: OpenAI model identifier.

    Returns:
        JSON dict with extracted entities grouped by type.
    """
    if entity_types:
        type_list = ", ".join(entity_types)
        schema = (
            f"A JSON object with keys for each entity type ({type_list}). "
            f"Each key maps to a list of extracted values of that type."
        )
    else:
        schema = (
            "A JSON object with keys: 'persons', 'organizations', 'locations', "
            "'dates', 'monetary_values', each mapping to a list of strings."
        )

    return extract_json(text, schema_description=schema, model=model)


def extract_key_value_pairs(
    text: str,
    fields: list,
    model: str = "gpt-4o",
) -> Dict[str, Any]:
    """Extract specific key-value pairs from text using OpenAI gpt-4o.

    Args:
        text: Source text.
        fields: List of field names to extract.
        model: OpenAI model identifier.

    Returns:
        JSON dict with the requested fields.
    """
    field_str = ", ".join(fields)
    schema = f"A JSON object with keys: {field_str}. Extract values from the text for each key."

    return extract_json(text, schema_description=schema, model=model)


if __name__ == "__main__":
    sample = (
        "John Smith, CEO of Acme Corporation based in New York, announced on "
        "January 15, 2024 that the company secured $50 million in Series C funding."
    )
    result = extract_entities(sample)
    print(json.dumps(result, indent=2))
