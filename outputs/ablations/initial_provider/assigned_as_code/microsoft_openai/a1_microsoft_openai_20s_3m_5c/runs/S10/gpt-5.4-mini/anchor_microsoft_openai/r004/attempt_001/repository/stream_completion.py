from model_client import get_client, get_model


def stream_completion(payload, config=None):
    config = config or {}
    with get_client(config) as client:
        stream = client.chat.completions.create(model=get_model(config), messages=[{'role': 'user', 'content': payload['prompt']}], stream=True)
        text = ''
        for chunk in stream:
            delta = chunk.choices[0].delta.content or ''
            text += delta
    return {'text': text}
