from model_client import get_generative_model
from model_models import ModelResponse
import json

def extract_json(text: str) -> ModelResponse:
    model = get_generative_model("gemini-pro")
    prompt = f"Extract JSON from the following text. Only return the JSON object.\n\n{text}"
    response = model.generate_content(prompt)
    # Assuming the model returns valid JSON directly in response.text
    return ModelResponse(text=response.text)
