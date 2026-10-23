import google.auth
from google.cloud import translate_v2 as translate


def runbook_translate(payload, config=None):
    credentials, project = google.auth.default()
    translate_client = translate.Client(credentials=credentials)
    result = translate_client.translate(payload['runbook_text'], target_language=payload['target_language'])
    return {"translated_text": result['translatedText']}