import os
from typing import Dict, Any
import requests
from document_models import FieldExtractionResponse


def extract_fields(text: str, schema: Dict[str, Any]) -> FieldExtractionResponse:
    """
    Extract structured fields from OCR-normalized document text using OpenAI GPT-4.
    """
    openai_api_key = os.getenv("OPENAI_API_KEY")
    
    prompt = f"Extract the following fields from the document text:\n\n{schema}\n\nDocument text:\n{text}"
    
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {openai_api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": "gpt-4",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3
        }
    )
    
    response.raise_for_status()
    result = response.json()
    
    # Parse the response content into fields
    fields = {}
    content = result["choices"][0]["message"]["content"]
    for line in content.split("\n"):
        if ":" in line:
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip()
    
    return FieldExtractionResponse(fields=fields, provider="openai_gpt4")