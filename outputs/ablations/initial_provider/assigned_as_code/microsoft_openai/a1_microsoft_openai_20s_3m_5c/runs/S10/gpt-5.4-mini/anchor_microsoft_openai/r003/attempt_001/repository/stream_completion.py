from openai import OpenAI

from model_client import build_messages, get_client, get_model


def stream_completion(payload, config=None):
    client = get_client(config)
    model = get_model(config)
    response = client.chat.completions.create(
        model=model,
        messages=build_messages(payload.get('system_prompt', ''), payload['prompt']),
        stream=True,
    )
    chunks = []
    for event in response:
        delta = event.choices[0].delta.content if event.choices else None
        if delta:
            chunks.append(delta)
    return {'text': ''.join(chunks)}
