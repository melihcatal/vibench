from google.cloud import firestore

from identity_client import load_identity_config, require_config


def profile_note_store(payload, config=None):
    config = require_config(load_identity_config(config), 'gcp_project_id')
    client = firestore.Client(project=config['gcp_project_id'])
    doc = client.collection('onboarding_notes').document(payload['user_id'])
    doc.set({'notes': payload.get('notes', ''), 'metadata': payload.get('metadata', {})}, merge=True)
    return {'stored': True, 'document_id': payload['user_id']}
