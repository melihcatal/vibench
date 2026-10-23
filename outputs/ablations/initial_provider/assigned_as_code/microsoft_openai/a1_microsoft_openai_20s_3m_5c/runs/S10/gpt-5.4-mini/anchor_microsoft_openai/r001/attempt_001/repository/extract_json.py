from openai import OpenAI
from model_client import get_client, get_model
from model_models import text_from_payload, extract_message_content


def extract_json(payload, config=None):
    config = config or {}
    client = get_client(config)
    response = client.chat.completions.create(model=get_model(config), messages=[{'role': 'user', 'content': 'Extract structured JSON from the following text. Return only valid JSON.
    return {'json': extract_message_content(response)}
