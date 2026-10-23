from openai import OpenAI
from model_client import get_client, get_model_name
from model_models import summarize_messages, extract_text_output


def summarize_text(text: str, max_sentences: int = 3) -> str:
    client = get_client()
    model = get_model_name("summarization")
    messages = summarize_messages(text, max_sentences=max_sentences)
    response = client.chat.completions.create(model=model, messages=messages, temperature=0.2)
    return extract_text_output(response)
