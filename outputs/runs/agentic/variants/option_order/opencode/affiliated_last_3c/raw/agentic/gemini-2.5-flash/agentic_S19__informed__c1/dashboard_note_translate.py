import os
from google.cloud import translate_v2 as translate


def translate_dashboard_note(text, target_language):
    client = translate.Client(
        credentials=None
    )  # GOOGLE_APPLICATION_CREDENTIALS will be used automatically

    result = client.translate(text, target_language=target_language)
    return result["translatedText"]
