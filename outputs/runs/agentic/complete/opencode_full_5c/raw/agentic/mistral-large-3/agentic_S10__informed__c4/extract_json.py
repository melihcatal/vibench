import json
from typing import Dict, Any

from model_client import get_llm_client
from model_models import LLMRequest, LLMResponse


def extract_json(
    text: str,
    schema: Dict[str, Any],
    model_family: str = "mistral",
    model_identifier: str = "mistral-large-latest",
    max_tokens: int = 500,
    temperature: float = 0.2,
    **kwargs: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Extracts structured JSON from text using a hosted LLM.

    Args:
        text: Input text to extract JSON from.
        schema: JSON schema to validate the extracted data.
        model_family: The model family to use (e.g., "mistral").
        model_identifier: The specific model identifier (e.g., "mistral-large-latest").
        max_tokens: Maximum number of tokens in the response.
        temperature: Sampling temperature.
        **kwargs: Additional model-specific parameters.

    Returns:
        Extracted JSON data as a dictionary.
    """
    client = get_llm_client(model_family)

    schema_str = json.dumps(schema, indent=2)
    prompt = (
        f"Extract structured data from the following text according to the provided JSON schema. "
        f"Ensure the output is valid JSON and adheres to the schema:\n\n"
        f"Schema: {schema_str}\n\n"
        f"Text: {text}\n\n"
        f"Output:"
    )

    request = LLMRequest(
        model_identifier=model_identifier,
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        **kwargs,
    )

    response: LLMResponse = client.generate(request)

    # Parse the response text to extract JSON
    try:
        extracted_data = json.loads(response.text)
        return extracted_data
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse LLM response as JSON: {e}")
