import json
import os
from typing import Dict, Any, Optional
from model_client import get_llm_client
from model_models import ExtractionRequest, ExtractionResponse


def extract_json(
    text: str,
    schema: Dict[str, Any],
    model: Optional[str] = "mistralai/Mistral-7B-Instruct-v0.2"
) -> Dict[str, Any]:
    """
    Extract structured JSON from text using a hosted LLM.
    Uses Together.ai's hosted Mistral 7B Instruct model by default.
    """
    client = get_llm_client()
    request = ExtractionRequest(
        input_text=text,
        schema=schema,
        model=model
    )
    response = client.post(
        "/inference",
        json=request.dict(),
        headers={"Authorization": f"Bearer {os.getenv('TOGETHER_API_KEY')}"}
    )
    response.raise_for_status()
    result = ExtractionResponse(**response.json())
    return json.loads(result.extracted_json)