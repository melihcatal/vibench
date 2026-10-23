import requests

from identity_client import load_identity_config, require_config
from identity_models import normalize_text


def profile_moderation(payload, config=None):
    config = load_identity_config(config)
    require_config(config, 'moderation_endpoint', 'moderation_key')
    text = normalize_text((payload or {}).get('text'))
    response = requests.post(
        f"{config['moderation_endpoint']}/contentsafety/text:analyze?api-version=2024-02-15-preview",
        headers={'Content-Type': 'application/json', 'Ocp-Apim-Subscription-Key': config['moderation_key']},
        json={'text': text},
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    return {'flagged': bool(data.get('jailbreakAnalysis', {}).get('detected')) or bool(data.get('sexualAnalysis', {}).get('detected')) or bool(data.get('violenceAnalysis', {}).get('detected')), 'result': data}
