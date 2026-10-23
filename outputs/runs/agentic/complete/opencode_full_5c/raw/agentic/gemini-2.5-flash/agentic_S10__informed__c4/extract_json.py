from model_client import call_gemini_generate_content
from model_models import ExtractJsonRequest, LLMResponse
import json
from typing import Dict, Any


def extract_json(
    text: str, json_schema: Dict[str, Any], model_name: str = "gemini-pro"
) -> LLMResponse:
    prompt = f"Extract information from the following text into a JSON object conforming to this schema: {json.dumps(json_schema)}\n\nText: {text}\n\nJSON:"
    request = ExtractJsonRequest(
        prompt=prompt, json_schema=json_schema, model_name=model_name
    )
    return call_gemini_generate_content(request)
