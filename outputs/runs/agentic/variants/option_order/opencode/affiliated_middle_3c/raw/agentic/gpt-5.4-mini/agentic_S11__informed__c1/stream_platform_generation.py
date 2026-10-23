from openai import OpenAI
from model_client import get_openai_client, resolve_model_name
from model_models import build_chat_messages, normalize_text


def stream_platform_generation(
    prompt: str, system_prompt: str = None, model: str = None
):
    client = get_openai_client()
    model_name = resolve_model_name(model)
    messages = build_chat_messages(prompt, system_prompt)
    stream = client.chat.completions.create(
        model=model_name, messages=messages, stream=True
    )
    chunks = []
    response_objects = []
    for chunk in stream:
        response_objects.append(chunk)
        delta = chunk.choices[0].delta.content if chunk.choices else None
        if delta:
            chunks.append(delta)
    return {
        "model": model_name,
        "output": normalize_text("".join(chunks)),
        "stream": response_objects,
    }
