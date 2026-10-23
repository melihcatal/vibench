from openai import OpenAI
from model_client import get_client, get_model_name
from model_models import safety_messages, parse_json_text, extract_text_output


def prompt_safety(text: str) -> dict:
    client = get_client()
    model = get_model_name("safety")
    messages = safety_messages(text)
    response = client.chat.completions.create(model=model, messages=messages, temperature=0.0)
    raw = extract_text_output(response)
    return parse_json_text(raw)
