from typing import Optional, Dict, Any
import os
import json
from model_client import get_llm_client
from model_models import ExtractionRequest, ExtractionResponse


def extract_json(
    text: str,
    json_schema: Dict[str, Any],
    max_tokens: int = 500,
    temperature: float = 0.2,
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Extract structured JSON from text using OpenAI's gpt-4o-mini model.
    """
    client = get_llm_client(
        api_key=api_key or os.getenv("OPENAI_API_KEY"),
        base_url=base_url or os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
    )

    schema_str = json.dumps(json_schema)
    request = ExtractionRequest(
        model=model or "gpt-4o-mini",
        text=text,
        max_tokens=max_tokens,
        temperature=temperature,
        system_prompt=f"Extract structured data matching this JSON schema: {schema_str}. Respond ONLY with valid JSON.",
    )

    response = client.create_completion(request)
    return ExtractionResponse(**response).extracted_json
