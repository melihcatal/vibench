import os
from typing import Dict, Any
import requests
from document_models import FieldExtractionResponse


def extract_fields(text: str, field_schema: Dict[str, str]) -> FieldExtractionResponse:
    """
    Extract structured fields from OCR-normalized document text using OpenAI GPT-3.5.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    
    # Construct prompt for field extraction
    prompt = f"Extract the following fields from the document text:\n"
    for field, description in field_schema.items():
        prompt += f"- {field}: {description}\n"
    prompt += f"\nDocument text:\n{text}\n\nExtracted fields (JSON format):"
    
    # OpenAI API-specific request
    request_payload = {
        "model": "gpt-3.5-turbo-1106",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
        "max_tokens": 500
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        json=request_payload,
        headers=headers
    )
    response.raise_for_status()
    
    result = response.json()
    extracted_fields = {}
    try:
        # Parse the JSON response from the model
        import json
        response_content = result["choices"][0]["message"]["content"].strip()
        extracted_fields = json.loads(response_content)
    except Exception as e:
        extracted_fields = {}
    
    return FieldExtractionResponse(
        fields=extracted_fields,
        provider="openai_gpt3.5",
        raw_response=result
    )