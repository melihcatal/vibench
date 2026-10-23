from google.cloud import translate_v2 as translate

def compliance_note_translate(note, target_language):
    client = translate.Client()
    result = client.translate(note, target_language=target_language)
    return {"translated_note": result['translatedText']}