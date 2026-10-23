from model_client import generate_text
from model_models import normalize_structured_json_response


def extract_json(payload, config=None):
    prompt = "Extract structured JSON from the following text. Return only valid JSON.\n\n" + payload["text"]
    response = generate_text(prompt, config=config)
    return normalize_structured_json_response(response)
