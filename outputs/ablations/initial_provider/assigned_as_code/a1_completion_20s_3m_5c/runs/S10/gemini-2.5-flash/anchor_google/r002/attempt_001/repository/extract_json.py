import json
from model_client import GeminiClient
from model_models import ModelPayload, ModelResponse

def extract_json(payload: ModelPayload) -> ModelResponse:
    client = GeminiClient()
    model = client.get_generative_model(model_name="gemini-pro") # gemini-pro is good for structured output
    
    prompt = f"Extract JSON from the following text. The JSON should represent key-value pairs of important information.\n\nText: {payload.text}\n\nJSON:"
    
    response = model.generate_content(prompt)
    
    try:
        extracted_content = json.loads(response.text)
    except json.JSONDecodeError:
        extracted_content = {"error": "Could not parse JSON", "raw_output": response.text}
        
    return ModelResponse(text=response.text, extracted_content=extracted_content)
