import requests

from identity_client import load_identity_config, require_config
from identity_models import normalize_locale


def welcome_translate(payload, config=None):
    config = require_config(load_identity_config(config), 'deepl_api_key')
    locale = normalize_locale(payload.get('locale'), config.get('locale', 'en'))
    response = requests.post('https://api-free.deepl.com/v2/translate', data={'auth_key': config['deepl_api_key'], 'text': payload['copy'], 'target_lang': locale.upper()[:2]}, timeout=30)
    response.raise_for_status()
    data = response.json()
    return {'locale': locale, 'translation': data['translations'][0]['text']}
