import os
import google.generativeai as genai
from model_client import get_gemini_model

def extract_json(text: str, schema: dict, model_name: str = "gemini-pro") -> dict:
    """
    Calls Google Gemini API to extract structured JSON from text.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = get_gemini_model(model_name)
    prompt = f"Extract information from the following text into a JSON object matching this schema: {schema}\n\nText: {text}\n\nJSON:"
    response = model.generate_content(prompt)
    # Assuming the model returns valid JSON directly in text
    import json
    try:
        return json.loads(response.text)
    except json.JSONDecodeError:
        print(f"Warning: Could not decode JSON from model output: {response.text}")
        return {}
