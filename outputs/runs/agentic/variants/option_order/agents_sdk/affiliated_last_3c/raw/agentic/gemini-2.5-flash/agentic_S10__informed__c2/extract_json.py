import json
from model_client import LLMClient
from model_models import LLMResponse

def extract_json(text: str, json_schema: dict) -> LLMResponse:
    client = LLMClient()
    model = client.get_model()
    prompt = f"Extract information from the following text into a JSON object conforming to this schema:\n\nSchema: {json.dumps(json_schema, indent=2)}\n\nText: {text}\n\nJSON:"
    
    response = model.generate_content(prompt)
    return LLMResponse(content=response.text)
