import requests

from security_models import normalize_text


def compliance_note_translate(payload, config=None):
    config = config or {}
    text = normalize_text(payload.get('note'))
    response = requests.post(
        f"{config['endpoint']}/translate?api-version=3.0&to={config['to_language']}",
        headers={
            'Ocp-Apim-Subscription-Key': config['key'],
            'Ocp-Apim-Subscription-Region': config['region'],
            'Content-Type': 'application/json',
        },
        json=[{'text': text}],
        timeout=30,
    )
    return response.json()
