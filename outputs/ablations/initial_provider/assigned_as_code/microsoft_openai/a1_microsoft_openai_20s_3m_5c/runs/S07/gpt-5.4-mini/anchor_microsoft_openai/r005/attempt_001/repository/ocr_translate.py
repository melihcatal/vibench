import requests

from document_models import normalize_text


def ocr_translate(payload, config=None):
    config = config or {}
    text = normalize_text(payload.get('text'))
    params = {'api-version': '3.0', 'from': payload.get('source_language', 'en'), 'to': payload.get('target_language', 'en')}
    headers = {'Ocp-Apim-Subscription-Key': config['translation_key'], 'Ocp-Apim-Subscription-Region': config.get('translation_region', 'global'), 'Content-Type': 'application/json'}
    response = requests.post(f"{config['translation_endpoint']}/translate", params=params, headers=headers, json=[{'text': text}])
    response.raise_for_status()
    data = response.json()
    return {'translation': data[0]['translations'][0]['text']}
