import requests

from identity_client import load_identity_config, require_config
from identity_models import build_note_document


def profile_note_store(payload, config=None):
    config = load_identity_config(config)
    require_config(config, 'support_project')
    document = build_note_document(payload)
    response = requests.post(
        'https://api.openai.com/v1/responses',
        headers={'Authorization': f"Bearer {config['support_project']}", 'Content-Type': 'application/json'},
        json={'model': 'gpt-5.4-mini', 'input': [{'role': 'system', 'content': 'Persist onboarding notes and support metadata.'}, {'role': 'user', 'content': str(document)}]},
        timeout=30,
    )
    response.raise_for_status()
    return {'stored': True, 'note': document.get('note'), 'provider_response': response.json()}
