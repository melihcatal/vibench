import json
from typing import Optional, Dict, Any

from model_client import get_model_client
from model_models import ModelRequest, ModelResponse, normalize_request, parse_response


def extract_json(
    text: str,
    json_schema: Dict[str, Any],
    model_family: Optional[str] = None,
    max_tokens: Optional[int] = None,
    temperature: Optional[float] = None,
    **kwargs,
) -> Dict[str, Any]:
    """Extract structured JSON from text using Mistral Chat API."""
    client = get_model_client()

    schema_str = json.dumps(json_schema, indent=2)
    request = ModelRequest(
        prompt=f"Extract structured data from the following text according to this JSON schema:\n\nSchema:\n{schema_str}\n\nText:\n{text}\n\nRespond ONLY with valid JSON matching the schema above.",
        model_family=model_family or "mistral",
        max_tokens=max_tokens or 500,
        temperature=temperature or 0.2,
        **kwargs,
    )

    normalized_request = normalize_request(request)
    response = client.chat_completion(normalized_request)
    parsed_response = parse_response(response)

    json_str = parsed_response.choices[0].message.content.strip()
    if json_str.startswith("```json"):
        json_str = json_str.split("```json")[1].split("```")[0].strip()
    elif json_str.startswith("```"):
        json_str = json_str.split("```")[1].split("```")[0].strip()

    return json.loads(json_str)
