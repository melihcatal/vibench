import os
from google.cloud import translate_v2 as translate


def appeal_translate(text, target_language):
    client = translate.Client(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
    result = client.translate(text, target_language=target_language)
    return result["translatedText"]
