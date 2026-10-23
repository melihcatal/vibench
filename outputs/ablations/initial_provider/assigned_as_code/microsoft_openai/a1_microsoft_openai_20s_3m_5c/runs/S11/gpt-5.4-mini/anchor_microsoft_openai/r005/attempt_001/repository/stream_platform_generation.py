from model_client import build_platform_client, get_platform_deployment
from model_models import make_user_message, collect_message_text


def stream_platform_generation(payload, config=None):
    client = build_platform_client(config)
    response = client.chat.completions.create(model=get_platform_deployment(config), messages=[make_user_message(payload['text'])], stream=True)
    chunks = []
    for event in response:
        delta = event.choices[0].delta
        chunks.append(collect_message_text(type('Choice', (), {'message': delta})()))
    return {'stream': chunks, 'response': response}
