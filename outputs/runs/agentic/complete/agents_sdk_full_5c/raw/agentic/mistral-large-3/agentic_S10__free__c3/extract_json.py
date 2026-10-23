import json
from typing import Dict, Any
from model_client import get_llm_client
from model_models import ExtractionRequest, ExtractionResponse

def extract_json(text: str, schema: Dict[str, Any]) -> Dict[str, Any]:
    """Extract structured JSON from text using OpenAI's GPT-4o-mini model."""
    client = get_llm_client()
    request = ExtractionRequest(
        model="gpt-4o-mini",
        text=text,
        schema=schema
    )
    response = client.extract(request)
    return json.loads(response.extracted_json)