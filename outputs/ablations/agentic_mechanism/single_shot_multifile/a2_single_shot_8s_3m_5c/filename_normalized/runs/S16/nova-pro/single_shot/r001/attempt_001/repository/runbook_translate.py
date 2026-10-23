import os
from google.cloud import secretmanager
from google.cloud import translate_v2 as translate

def translate_runbook(project_id, secret_id, target_language):
    client = secretmanager.SecretManagerServiceClient()
    name = f'projects/{project_id}/secrets/{secret_id}'
    secret = client.get_secret(name=name)
    notes = secret.annotations.get('runbook_notes', '')
    translate_client = translate.Client()
    result = translate_client.translate(notes, target_language=target_language)
    return result['translatedText']

if __name__ == '__main__':
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    secret_id ='my-secret'
    target_language = 'es'
    print(translate_runbook(project_id, secret_id, target_language))