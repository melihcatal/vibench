import google.generativeai as genai
from model_client import get_generative_model
from model_models import GeminiModel
import json


def extract_json(text: str, schema_hint: dict) -> dict:
    """Calls a hosted LLM to extract structured JSON from text."""
    model = get_generative_model(GeminiModel.JSON_EXTRACTION)
    prompt = f"Extract information from the following text as JSON, conforming to this schema hint:\n\nSchema Hint: {json.dumps(schema_hint, indent=2)}\n\nText: {text}\n\nJSON:"
    response = model.generate_content(prompt)
    try:
        return json.loads(response.text)
    except json.JSONDecodeError:
        # Attempt to clean the response if it's not pure JSON
        # This is a very basic attempt and might need more robust error handling
        cleaned_text = response.text.strip().strip("`")
        if cleaned_text.startswith("json\n"):
            cleaned_text = cleaned_text[4:].strip()
        try:
            return json.loads(cleaned_text)
        except json.JSONDecodeError:
            raise ValueError(
                f"Could not decode JSON from model response: {response.text}"
            )
