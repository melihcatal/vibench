from openai import OpenAI
from model_client import get_client, get_model_name
from model_models import spoken_brief_messages, extract_text_output


def spoken_brief(text: str) -> str:
    client = get_client()
    model = get_model_name("speech")
    messages = spoken_brief_messages(text)
    response = client.chat.completions.create(model=model, messages=messages, temperature=0.4)
    return extract_text_output(response)
