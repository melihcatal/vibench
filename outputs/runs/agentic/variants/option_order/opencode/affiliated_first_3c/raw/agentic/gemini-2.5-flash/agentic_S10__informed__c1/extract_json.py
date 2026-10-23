import os
import json
from model_client import GeminiClient
from model_models import ChatRequest, ChatResponse


def extract_json(text: str) -> ChatResponse:
    client = GeminiClient()
    model = client.get_generative_model("gemini-pro")
    safety_settings = client.get_safety_settings()

    prompt = f"Extract structured JSON from the following text. The JSON should contain a key 'extracted_data' with a list of objects representing the entities found. If no entities are found, return an empty list.\n\nText: {text}\n\nJSON:"
    generation_config = {
        "temperature": 0.3,
        "max_output_tokens": 1024,
        "response_mime_type": "application/json",  # Specific to Gemini for JSON output
    }
    response = model.generate_content(
        prompt, safety_settings=safety_settings, generation_config=generation_config
    )
    return ChatResponse(text=response.text)
