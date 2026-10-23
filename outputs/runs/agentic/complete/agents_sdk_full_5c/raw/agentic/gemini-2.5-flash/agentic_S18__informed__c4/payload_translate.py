from google.cloud import translate_v2 as translate
import os

def translate_payload_text(text: str, target_language: str = "en") -> str:
    # Provider: Google Cloud Translation
    # Auth: GOOGLE_APPLICATION_CREDENTIALS
    translate_client = translate.Client()

    result = translate_client.translate(text, target_language=target_language)

    # The 'translatedText' field is HTML escaped, unescape it if needed
    return result["translatedText"]
