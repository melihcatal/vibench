from openai import OpenAI
from model_client import get_client, get_model_name
from model_models import extraction_messages, parse_json_text


def extract_json(text: str) -> dict:
    client = get_client()
    model = get_model_name("extraction")
    messages = extraction_messages(text)
    response = client.chat.completions.create(model=model, messages=messages, temperature=0.0)
    return parse_json_text(response.choices[0].message.content or "")
