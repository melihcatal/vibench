from openai import OpenAI
from model_client import get_client, get_model_name
from model_models import translation_messages, extract_text_output


def result_translate(text: str, target_language: str) -> str:
    client = get_client()
    model = get_model_name("translation")
    messages = translation_messages(text=text, target_language=target_language)
    response = client.chat.completions.create(model=model, messages=messages, temperature=0.2)
    return extract_text_output(response)
