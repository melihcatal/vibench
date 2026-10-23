from google import genai

from model_client import get_api_key, get_model
from model_models import normalize_json_response


def extract_json(payload, config=None):
    config = config or {}
    prompt = payload["text"] + "\n\nReturn only valid JSON for the requested structure."
    with genai.Client(api_key=get_api_key(config)) as client:
        response = client.models.generate_content(model=get_model(config), contents=prompt)
    return normalize_json_response(response.text)
