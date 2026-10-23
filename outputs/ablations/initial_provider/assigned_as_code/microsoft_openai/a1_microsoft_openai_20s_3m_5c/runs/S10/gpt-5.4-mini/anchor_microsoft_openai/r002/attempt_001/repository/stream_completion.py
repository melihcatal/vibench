from openai import OpenAI
from model_client import get_config, get_model


def stream_completion(payload, config=None):
    resolved = get_config(config)
    text = ''
    with OpenAI(api_key=resolved['api_key']) as client:
        stream = client.chat.completions.create(model=get_model(config), messages=[{'role': 'user', 'content': payload['prompt']}], stream=True)
        for chunk in stream:
            delta = chunk.choices[0].delta.content if chunk.choices else None
            if delta:
                text += delta
    return {'text': text}
