from model_client import get_client, get_model
from model_models import get_input_text


def stream_completion(payload, config=None):
    client = get_client(config)
    text = get_input_text(payload)
    stream = client.chat.completions.create(model=get_model(config), messages=[{'role': 'user', 'content': text}], stream=True)
    return {'chunks': [chunk.choices[0].delta.content for chunk in stream if getattr(chunk.choices[0].delta, 'content', None)]}
