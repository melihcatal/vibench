import os
from google.cloud import translate_v2 as translate


def translate_invoice_note(text: str, target_language: str = "en") -> str:
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")

    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return result["translatedText"]
