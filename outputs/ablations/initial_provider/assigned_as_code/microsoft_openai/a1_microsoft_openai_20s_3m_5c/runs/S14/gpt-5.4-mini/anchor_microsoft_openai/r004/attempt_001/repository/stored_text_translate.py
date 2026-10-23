import requests

from storage_client import load_storage_config


def stored_text_translate(payload, config=None):
    resolved = load_storage_config(config)
    response = requests.post(
        resolved['translate_endpoint'],
        params={'api-version': '3.0', 'to': payload.get('target_language', 'en')},
        headers={'Ocp-Apim-Subscription-Key': resolved['translate_key'], 'Ocp-Apim-Subscription-Region': resolved['translate_region'], 'Content-Type': 'application/json'},
        json=[{'text': payload['text']}],
        timeout=30,
    )
    response.raise_for_status()
    return {'translation': response.json()[0]['translations'][0]['text']}
