from model_client import build_platform_client, get_platform_deployment
from model_models import make_user_message


def collect_platform_metadata(payload, config=None):
    client = build_platform_client(config)
    response = client.chat.completions.create(model=get_platform_deployment(config), messages=[make_user_message(payload['text'])])
    return {'text': response.choices[0].message.content or '', 'usage': getattr(response, 'usage', None), 'model': getattr(response, 'model', None), 'id': getattr(response, 'id', None)}
