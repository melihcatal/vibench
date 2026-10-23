import os
from openai import OpenAI
from model_client import get_chat_client, select_chat_model, chat_messages, chat_text


def summarize_text(text: str) -> str:
    client = get_chat_client()
    model = select_chat_model('summarization')
    response = client.chat.completions.create(
        model=model,
        messages=chat_messages('Summarize the following text concisely.', text),
        temperature=0.2,
    )
    return chat_text(response)
