from openai import OpenAI

from identity_client import load_identity_config
from identity_models import build_locale_payload


def welcome_translate(payload, config=None):
    config = load_identity_config(config)
    payload = build_locale_payload(payload)
    client = OpenAI(api_key=config.openai_api_key)
    response = client.responses.create(model='gpt-5.4-mini', input=f"Translate into {payload['locale']}: {payload['text']}")
    return {'locale': payload['locale'], 'translation': response.output_text}
