from google.cloud import translate_v2 as translate

def dashboard_note_translate(payload, config=None):
    config = config or {}
    client = translate.Client()
    result = client.translate(payload['note'], target_language=payload['target_language'])
    return {"translated_note": result['translatedText']}