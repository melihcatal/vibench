import json
import os
from typing import Dict, Any
from model_client import get_dashscope_client
from model_models import ExtractionRequest, ExtractionResponse

def extract_json(
    text: str,
    schema: Dict[str, Any],
    model: str = "qwen-turbo",
    temperature: float = 0.3,
) -> Dict[str, Any]:
    """
    Extract structured JSON from text using DashScope Qwen model.
    
    Args:
        text: Input text to extract data from.
        schema: JSON schema defining the expected structure.
        model: Model identifier (e.g., "qwen-turbo", "qwen-plus").
        temperature: Sampling temperature.
    
    Returns:
        Extracted data as a dictionary.
    """
    client = get_dashscope_client()
    
    schema_str = json.dumps(schema, indent=2)
    prompt = (
        f"Extract structured data from the following text according to the schema below. "
        f"Respond only with valid JSON matching the schema.\n\n"
        f"Text: {text}\n\n"
        f"Schema: {schema_str}"
    )
    
    request = ExtractionRequest(
        model=model,
        prompt=prompt,
        temperature=temperature,
    )
    
    response = client.call_model(request)
    output = ExtractionResponse(**response).output
    return json.loads(output)