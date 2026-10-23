import google.cloud.translate


def translate_runbook_notes(payload, config=None):
    config = config or {}
    translate_client = google.cloud.translate.Client()
    translation = translate_client.translate(payload['notes'], target_language='es')
    return {"translated_notes": translation['translatedText']}