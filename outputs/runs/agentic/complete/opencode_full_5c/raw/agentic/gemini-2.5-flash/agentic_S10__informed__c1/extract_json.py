import os
import google.generativeai as genai
from model_client import get_gemini_client


def extract_json(text: str, schema: dict) -> dict:
    """
    Calls Google Gemini API to extract structured JSON from text.
    The schema parameter is a dictionary representing the desired JSON structure.
    """
    client = get_gemini_client()
    model = client.GenerativeModel("gemini-pro")
    prompt = f"Extract information from the following text into a JSON object matching this schema:\n\nSchema: {schema}\n\nText: {text}\n\nJSON:"
    response = model.generate_content(prompt)
    # Assuming the model returns valid JSON directly
    import json

    return json.loads(response.text)
