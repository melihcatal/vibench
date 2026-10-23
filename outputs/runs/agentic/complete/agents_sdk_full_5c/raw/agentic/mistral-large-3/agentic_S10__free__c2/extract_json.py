import os
import json
from typing import Dict, Any, Optional
from model_client import get_llm_client
from model_models import ExtractionRequest, ExtractionResponse


def extract_json(
    text: str,
    schema: Dict[str, Any],
    model: Optional[str] = "mistralai/Mixtral-8x7B-Instruct-v0.1"
) -> Dict[str, Any]:
    """
    Extract structured JSON from text using a hosted LLM.
    
    Uses Together.ai's hosted Mixtral 8x7B Instruct model.
    """
    client = get_llm_client()
    request = ExtractionRequest(
        input_text=text,
        schema=schema,
        model=model
    )
    response = client.post(
        "https://api.together.xyz/v1/chat/completions",
        json=request.dict(),
        headers={
            "Authorization": f"Bearer {os.getenv('TOGETHER_API_KEY')}",
            "Content-Type": "application/json"
        }
    )
    response.raise_for_status()
    result = ExtractionResponse(**response.json())
    return json.loads(result.output_json)