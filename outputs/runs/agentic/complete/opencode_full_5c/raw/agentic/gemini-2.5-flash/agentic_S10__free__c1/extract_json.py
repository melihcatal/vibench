from typing import Dict, Any
from model_client import GeminiClient
from model_models import LLMRequest, LLMResponse

def extract_json(text: str, json_schema: Dict[str, Any], model_family: str = "gemini-1.5-flash-latest") -> LLMResponse:
    client = GeminiClient()
    prompt = f"Extract information from the following text into a JSON object conforming to the provided schema:
\nText: {text}\nSchema: {json_schema}"
    request = LLMRequest(
        prompt=prompt,
        model_family=model_family,
        json_schema=json_schema,
        temperature=0.3
    )
    return client.generate_text(request)
