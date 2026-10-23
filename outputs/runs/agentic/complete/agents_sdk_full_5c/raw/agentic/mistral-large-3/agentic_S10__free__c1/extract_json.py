import json
import os
from typing import Dict, Any
from model_client import get_llm_client
from model_models import ExtractionRequest, ExtractionResponse

def extract_json(
    text: str,
    schema: Dict[str, Any],
    model: str = "anthropic.claude-3-haiku-20240307-v1:0"
) -> Dict[str, Any]:
    """
    Extract structured JSON from text using Anthropic's Claude model.
    """
    client = get_llm_client()
    schema_str = json.dumps(schema, indent=2)
    request = ExtractionRequest(
        text=text,
        schema=schema,
        model=model
    )
    response = client.messages.create(
        model=request.model,
        max_tokens=4096,
        messages=[{"role": "user", "content": f"Extract JSON matching this schema from the text:\n\nSchema: {schema_str}\n\nText: {request.text}"}]
    )
    return ExtractionResponse.from_anthropic(response).extracted_data