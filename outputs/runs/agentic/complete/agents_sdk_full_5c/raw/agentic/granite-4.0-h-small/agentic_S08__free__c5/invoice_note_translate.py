from google.cloud import translate_v2 as translate

def invoice_note_translate(note: str, target_lang: str = "en") -> str:
    """Translate extracted invoice notes/description to target language using Google Cloud Translation."""
    translate_client = translate.Client()
    result = translate_client.translate(note, target_language=target_lang)
    return result["translatedText"]