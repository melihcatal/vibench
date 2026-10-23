import os
import json

from model_client import GeminiClient
from model_models import LLMResponse, TextCompletionRequest


def extract_json(
    text: str, schema: dict, model_name: str = "gemini-pro", temperature: float = 0.3
) -> LLMResponse:
    """Extracts structured JSON from text using a hosted LLM."""
    prompt = f"""Extract information from the following text into a JSON object that conforms to the provided JSON schema. Ensure the output is a valid JSON object. If a field is not found, use null.

Text: {text}

Schema: {json.dumps(schema, indent=2)}

JSON:"""

    client = GeminiClient()
    request = TextCompletionRequest(
        prompt=prompt,
        model_name=model_name,
        max_output_tokens=2000,  # Increased for potentially larger JSON outputs
        temperature=temperature,
    )
    response = client.text_completion(request)
    return response
