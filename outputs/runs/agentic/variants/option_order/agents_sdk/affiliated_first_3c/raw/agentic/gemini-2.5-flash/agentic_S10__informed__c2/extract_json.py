import os
import json
from model_client import get_gemini_client
from model_models import LLMResponse

def extract_json(text: str, model_id: str = 'gemini-pro') -> LLMResponse:
    client = get_gemini_client()
    prompt = f"Extract structured JSON from the following text. The JSON should represent key information within the text. Only return the JSON object.\n\nText: {text}"
    response = client.generate_content(prompt)
    # Attempt to parse the text as JSON. Gemini might return markdown wrapped JSON.
    try:
        extracted_text = response.text.strip()
        if extracted_text.startswith('```json') and extracted_text.endswith('```'):
            extracted_text = extracted_text[len('```json'):-len('```')].strip()
        json_data = json.loads(extracted_text)
        return LLMResponse(text=json.dumps(json_data), raw_response=response.to_dict())
    except json.JSONDecodeError:
        return LLMResponse(text=response.text, raw_response=response.to_dict()) # Return raw if not valid JSON

