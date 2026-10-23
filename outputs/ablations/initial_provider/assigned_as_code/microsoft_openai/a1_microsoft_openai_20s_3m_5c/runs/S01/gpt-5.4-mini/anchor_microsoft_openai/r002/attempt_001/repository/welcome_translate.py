import os

from openai import OpenAI

from identity_client import load_identity_config
from identity_models import normalize_locale, require_fields


def welcome_translate(payload, config=None):
    payload = require_fields(payload, ['text', 'locale'])
    config = load_identity_config(config)
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    result = client.responses.create(model='gpt-5.4-mini', input='Translate this onboarding copy into ' + normalize_locale(payload['locale']) + ': ' + payload['text'])
    return {'locale': normalize_locale(payload['locale']), 'translation': result.output_text}
