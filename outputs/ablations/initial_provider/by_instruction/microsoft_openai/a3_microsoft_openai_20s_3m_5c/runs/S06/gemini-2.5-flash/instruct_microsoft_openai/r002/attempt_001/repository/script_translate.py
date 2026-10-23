from google.cloud import translate_v2 as translate
import os

def translate_script(text: str, target_language: str, source_language: str | None = None) -> str:
    """
    Translates narration scripts using Google Cloud Translation API.
    """
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set for authentication
    # os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/path/to/your/keyfile.json"

    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target_language, source_language=source_language)

    return result['translatedText']
