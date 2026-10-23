import os
from google.cloud import translate_v2 as translate

def translate_runbook_notes(project_id, text, target_language):
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return result['translatedText']

if __name__ == '__main__':
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    text = 'Rotate the secret every 90 days.'
    target_language = 'es'
    print(translate_runbook_notes(project_id, text, target_language))