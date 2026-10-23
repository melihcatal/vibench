from google.cloud import translate_v2 as translate

def translate_text(text: str, target_language: str) -> str:
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return result['translatedText']

def dashboard_note_translate(note: str, target_language: str) -> str:
    return translate_text(note, target_language)