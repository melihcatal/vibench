import os
import json
from typing import Dict, Any, Optional
from model_client import get_mistral_client
from model_models import ExtractionRequest, ExtractionResponse


def extract_json(
    text: str,
    schema: Dict[str, Any],
    model: str = "mistral-small",
    temperature: float = 0.2
) -> ExtractionResponse:
    """
    Extract structured JSON from text using Mistral's hosted LLM.
    """
    client = get_mistral_client()
    schema_str = json.dumps(schema, indent=2)
    
    request = ExtractionRequest(
        text=text,
        schema=schema,
        model=model,
        temperature=temperature
    )
    
    response = client.chat.complete(
        model=request.model,
        messages=[
            {
                "role": "system", 
                "content": f"Extract data from the following text as JSON matching this schema:\n{schema_str}"
            },
            {"role": "user", "content": text}
        ],
        temperature=request.temperature
    )
    
    extracted_content = response.choices[0].message.content
    try:
        extracted_data = json.loads(extracted_content)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse extracted JSON: {e}")
    
    return ExtractionResponse(
        extracted_data=extracted_data,
        model=response.model,
        input_tokens=response.usage.prompt_tokens,
        output_tokens=response.usage.completion_tokens
    )