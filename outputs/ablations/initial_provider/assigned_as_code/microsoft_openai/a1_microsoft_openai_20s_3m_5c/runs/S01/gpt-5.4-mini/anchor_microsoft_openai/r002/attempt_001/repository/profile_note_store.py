import os

import requests

from identity_client import load_identity_config
from identity_models import require_fields


def profile_note_store(payload, config=None):
    payload = require_fields(payload, ['note', 'account_id'])
    config = load_identity_config(config)
    url = config['managed_store_url'] + '/dbs/onboarding/colls/notes/docs'
    response = requests.post(url, headers={'Authorization': 'Bearer ' + os.getenv('AZURE_DOCUMENTDB_KEY', ''), 'Content-Type': 'application/json'}, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()
