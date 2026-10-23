import json
from typing import Dict, Any, Optional
from model_client import get_llm_client
from model_models import ExtractionRequest, ExtractionResponse


def extract_json(
    text: str,
    schema: Dict[str, Any],
    model: Optional[str] = "gpt-4o-2024-05-13"
) -> Dict[str, Any]:
    """
    Extract structured JSON from text using OpenAI's GPT model.
    """
    client = get_llm_client()
    
    schema_str = json.dumps(schema, indent=2)
    prompt = (
        f"Extract structured data from the following text according to this JSON schema:\n"
        f"{schema_str}\n\n"
        f"Text: {text}\n\n"
        f"Respond with ONLY the JSON data, no other text or explanations."
    )
    
    request = ExtractionRequest(
        prompt=prompt,
        model=model,
        response_format={"type": "json_object"}
    )
    
    response = client.chat.completions.create(
        model=request.model,
        messages=[{"role": "user", "content": request.prompt}],
        response_format=request.response_format
    )
    
    return ExtractionResponse.from_openai(response).extracted_data