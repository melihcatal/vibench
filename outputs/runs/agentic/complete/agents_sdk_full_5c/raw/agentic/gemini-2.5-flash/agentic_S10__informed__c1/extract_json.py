import os
import google.generativeai as genai
from model_client import get_gemini_model

def extract_json(text: str, schema: dict, model_name: str = "gemini-pro") -> str:
    """
    Calls Google Gemini API to extract structured JSON from text.
    The schema should describe the expected JSON structure.
    """
    model = get_gemini_model(model_name)
    prompt = f"Extract information from the following text into a JSON object matching this schema:\n\nSchema: {schema}\n\nText: {text}\n\nJSON:"
    response = model.generate_content(prompt)
    return response.text

if __name__ == '__main__':
    # Example usage (requires GOOGLE_API_KEY env var)
    # sample_text = "Name: John Doe, Age: 30, City: New York"
    # sample_schema = {"type": "object", "properties": {"name": {"type": "string"}, "age": {"type": "integer"}, "city": {"type": "string"}}}
    # print(extract_json(sample_text, sample_schema))
    pass
