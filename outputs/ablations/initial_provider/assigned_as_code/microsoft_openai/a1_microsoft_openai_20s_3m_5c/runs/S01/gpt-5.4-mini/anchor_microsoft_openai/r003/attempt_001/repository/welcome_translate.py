import requests

from identity_client import load_identity_config, require_config
from identity_models import normalize_locale, normalize_text


def welcome_translate(payload, config=None):
    config = load_identity_config(config)
    require_config(config, 'translation_endpoint', 'translation_key', 'translation_region')
    payload = dict(payload or {})
    source_text = normalize_text(payload.get('text'))
    target_language = normalize_locale(payload.get('locale'))
    response = requests.post(
        f"{config['translation_endpoint']}/translate",
        params={'api-version': '3.0', 'to': target_language},
        headers={'Ocp-Apim-Subscription-Key': config['translation_key'], 'Ocp-Apim-Subscription-Region': config['translation_region'], 'Content-Type': 'application/json'},
        json=[{'text': source_text}],
        timeout=30,
    )
    response.raise_for_status()
    return {'locale': target_language, 'translation': response.json()[0]['translations'][0]['text']}
