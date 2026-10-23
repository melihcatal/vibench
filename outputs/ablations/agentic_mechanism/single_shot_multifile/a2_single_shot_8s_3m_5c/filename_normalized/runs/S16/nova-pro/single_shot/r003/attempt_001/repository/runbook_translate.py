from google.cloud import translate_v2 as translate

def translate_runbook_notes(notes, target_language):
    client = translate.Client()
    result = client.translate(notes, target_language=target_language)
    return result['translatedText']