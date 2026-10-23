import os
from openai import OpenAI
from model_client import get_openai_client, resolve_model_name
from model_models import build_chat_messages, normalize_text


def invoke_platform_model(prompt: str, system_prompt: str = None, model: str = None):
    client = get_openai_client()
    model_name = resolve_model_name(model)
    messages = build_chat_messages(prompt, system_prompt)
    response = client.chat.completions.create(model=model_name, messages=messages)
    choice = response.choices[0]
    text = normalize_text(choice.message.content)
    return {"model": model_name, "output": text, "response": response}
