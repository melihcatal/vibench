import os
import json
from model_client import get_gemini_client
from model_models import LLMResponse

def extract_json(text: str, json_schema: dict) -> LLMResponse:
    genai = get_gemini_client()
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"Extract information from the following text into a JSON object matching this schema:
{json.dumps(json_schema, indent=2)}

Text: {text}

JSON:"
    response = model.generate_content(prompt)
    return LLMResponse(text=response.text)
