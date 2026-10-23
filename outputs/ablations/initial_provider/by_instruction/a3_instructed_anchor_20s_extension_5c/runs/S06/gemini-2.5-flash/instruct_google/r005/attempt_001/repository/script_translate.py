from google.cloud import translate_v2 as translate

def translate_script(text: str, target_language: str, source_language: str = None) -> str:
    """Translates narration scripts using Google Cloud Translation."""
    client = translate.Client()

    # Target language must be provided.
    # Source language can be auto-detected if not provided.
    result = client.translate(text, target_language=target_language, source_language=source_language)

    return result['translatedText']
