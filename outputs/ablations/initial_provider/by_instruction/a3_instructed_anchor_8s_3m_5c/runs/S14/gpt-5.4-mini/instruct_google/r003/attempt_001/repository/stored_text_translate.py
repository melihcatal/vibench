from google.cloud import translate_v2 as translate


def translate_stored_text(text: str, target_language: str, source_language: str = None):
    client = translate.Client()
    result = client.translate(text, target_language=target_language, source_language=source_language)
    return result.get("translatedText", "")
