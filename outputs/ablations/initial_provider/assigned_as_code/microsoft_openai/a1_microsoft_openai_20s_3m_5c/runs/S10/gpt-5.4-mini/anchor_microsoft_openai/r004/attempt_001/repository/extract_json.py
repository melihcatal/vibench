from model_client import get_client, get_model
from model_models import extract_text, normalize_json_text


def extract_json(payload, config=None):
    config = config or {}
    with get_client(config) as client:
        response = client.chat.completions.create(model=get_model(config), messages=[{'role': 'user', 'content': 'Extract the requested structured JSON from the text and return only valid JSON:\n\n' + payload['text']}])
    return {'json': normalize_json_text(extract_text(response))}
