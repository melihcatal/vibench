import os
from google.cloud import translate_v2 as translate

def translate_runbook_notes(runbook_notes):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/your/service-account-file.json'
    translate_client = translate.Client()
    result = translate_client.translate(runbook_notes, target_language='en')
    return result['translatedText']

if __name__ == '__main__':
    runbook_notes = 'Enter your runbook notes here'
    translated_notes = translate_runbook_notes(runbook_notes)
    print(translated_notes)