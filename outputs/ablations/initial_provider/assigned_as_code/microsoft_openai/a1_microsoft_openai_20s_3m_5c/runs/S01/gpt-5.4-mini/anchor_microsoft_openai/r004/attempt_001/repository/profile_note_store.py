import requests


def profile_note_store(payload, config=None):
    config = config or {}
    base_url = config['firestore_base_url']
    document_path = payload['document_path']
    response = requests.patch(
        f'{base_url}/{document_path}',
        params={'updateMask.fieldPaths': 'note'},
        headers={'Authorization': f"Bearer {config['firestore_access_token']}", 'Content-Type': 'application/json'},
        json={'fields': {'note': {'stringValue': payload['note']}, 'metadata': {'mapValue': {'fields': {}}}}},
        timeout=30,
    )
    response.raise_for_status()
    return {'stored': True, 'name': response.json().get('name', document_path)}
