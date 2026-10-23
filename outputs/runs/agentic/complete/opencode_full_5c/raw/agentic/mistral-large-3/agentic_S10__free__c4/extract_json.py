from typing import Optional, Dict, Any
import json
import os
from model_client import get_llm_client
from model_models import ExtractionRequest, ExtractionResponse


def extract_json(
    text: str,
    json_schema: Dict[str, Any],
    max_tokens: int = 250,
    temperature: float = 0.2,
    model: Optional[str] = "mistral/mistral-large-latest",
) -> Dict[str, Any]:
    """
    Extracts structured JSON from text using a hosted LLM.

    Args:
        text: The input text to extract JSON from.
        json_schema: The JSON schema to enforce for the extraction.
        max_tokens: Maximum number of tokens in the extraction.
        temperature: Controls randomness in the extraction.
        model: The model identifier for the hosted LLM.

    Returns:
        The extracted JSON data as a dictionary.
    """
    client = get_llm_client()

    request = ExtractionRequest(
        input_text=text,
        json_schema=json_schema,
        max_tokens=max_tokens,
        temperature=temperature,
        model=model,
    )

    response = client.extract(request)
    return response.extracted_data
