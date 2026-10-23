import json
import os
from typing import Dict, Any, Optional
from model_client import get_llm_client
from model_models import ExtractionRequest, ExtractionResponse


def extract_json(
    text: str,
    schema: Dict[str, Any],
    model: Optional[str] = "gpt-4o-mini"
) -> Dict[str, Any]:
    """
    Extract structured JSON from text using OpenAI's hosted LLM.
    """
    client = get_llm_client()
    schema_str = json.dumps(schema, indent=2)
    request = ExtractionRequest(
        input_text=text,
        schema=schema,
        model=model
    )
    response = client.chat.completions.create(
        model=request.model,
        messages=[
            {
                "role": "system", 
                "content": f"Extract structured data matching this schema:\n{schema_str}\nRespond only with valid JSON."
            },
            {"role": "user", "content": f"Extract from:\n\n{request.input_text}"}
        ],
        temperature=0.1
    )
    return ExtractionResponse.from_openai(response).extracted_data