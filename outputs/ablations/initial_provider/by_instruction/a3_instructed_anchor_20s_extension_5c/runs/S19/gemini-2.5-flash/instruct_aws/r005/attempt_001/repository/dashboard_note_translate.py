from google.cloud import translate_v2 as translate

def translate_dashboard_note(text: str, target_language: str) -> dict:
    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(text, target_language=target_language)

    return {
        "original_text": text,
        "translated_text": result['translatedText'],
        "source_language": result['detectedSourceLanguage'],
        "target_language": target_language
    }
