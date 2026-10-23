import os
from ibm_watsonx_ai import WatsonxApi
import json

def runbook_translate(secret_id, note_field='notes', target_lang='es'):
    """Translates rotation runbook notes.
    Returns:
        str: Translated note.
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
    translation = wa.translate_text(text=note, target=target_lang)
    return translation['translations'][0]['translation']
