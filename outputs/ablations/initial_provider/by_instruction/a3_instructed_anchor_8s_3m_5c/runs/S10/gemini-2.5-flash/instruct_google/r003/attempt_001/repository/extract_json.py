from model_client import GoogleLLMClient
from model_models import LLMRequest, LLMResponse
import json

def extract_json(text: str, schema: dict, max_tokens: int = 500, temperature: float = 0.3) -> dict:
    client = GoogleLLMClient()
    prompt = f"Extract information from the following text as a JSON object adhering to this schema: {json.dumps(schema)}\n\nText: {text}\n\nJSON:"
    request = LLMRequest(prompt=prompt, max_tokens=max_tokens, temperature=temperature)
    response = client.generate_text(request)
    try:
        return json.loads(response.text)
    except json.JSONDecodeError:
        # Attempt to clean up and re-parse if the LLM output is not perfectly formed JSON
        # This is a simple heuristic and might need more robust error handling
        cleaned_text = response.text.strip().lstrip('`').rstrip('`').lstrip('json').strip()
        try:
            return json.loads(cleaned_text)
        except json.JSONDecodeError:
            return {"error": "Failed to extract valid JSON", "raw_output": response.text}
