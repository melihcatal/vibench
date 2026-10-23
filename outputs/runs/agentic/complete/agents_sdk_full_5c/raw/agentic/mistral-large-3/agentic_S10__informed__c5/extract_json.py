import os
import json
from typing import Dict, Any, Optional
from model_client import get_llm_client
from model_models import ExtractionRequest, ExtractionResponse


def extract_json(
    text: str,
    schema: Dict[str, Any],
    model_family: str = "gemini",
    model_id: str = "gemini-1.5-pro-001",
    temperature: float = 0.3,
    **kwargs
) -> Optional[Dict[str, Any]]:
    """
    Extract structured JSON from text using a hosted LLM.
    
    Args:
        text: Input text to extract from.
        schema: JSON schema describing the expected output structure.
        model_family: The model family to use (e.g., 'gemini').
        model_id: The specific model identifier (e.g., 'gemini-1.5-pro-001').
        temperature: Sampling temperature.
        **kwargs: Additional model-specific parameters.
        
    Returns:
        Extracted JSON as a dictionary or None if failed.
    """
    client = get_llm_client(model_family)
    if not client:
        return None

    request = ExtractionRequest(
        text=text,
        schema=schema,
        model_id=model_id,
        temperature=temperature,
        **kwargs
    )
    response = client.extract(request)
    if isinstance(response, ExtractionResponse) and response.json_data:
        try:
            return json.loads(response.json_data)
        except json.JSONDecodeError:
            return None
    return None