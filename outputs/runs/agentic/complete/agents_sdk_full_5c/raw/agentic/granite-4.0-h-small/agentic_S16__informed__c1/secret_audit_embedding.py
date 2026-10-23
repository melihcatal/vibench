import os
from ibm_secrets_manager_sdk import SecretsManagerV1
from ibm_watsonx_ai import WatsonxApi
import json

def secret_audit_embedding(secret_id, note_field='notes'):
    """Creates an embedding for a secret's audit note.
    Returns:
        dict: embedding vector and note text.
    """
    api_key = os.getenv('IBM_SECRETS_MANAGER_APIKEY')
    if not api_key:
        raise RuntimeError('IBM_SECRETS_MANAGER_APIKEY not set')
    client = SecretsManagerV1.new_instance(api_key=api_key)
    secret = client.get_secret(secret_id=secret_id).get_result()
    payload = secret.get('secret_data', '')
    data = json.loads(payload)
    note = data.get(note_field, '')
    wa = WatsonxApi(api_key=api_key, project_id=os.getenv('WATSONX_PROJECT_ID'))
    embedding = wa.embed_text(text=note)['embeddings'][0]['values']
    return {'embedding': embedding, 'note': note}
