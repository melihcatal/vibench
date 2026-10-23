import os
import google.auth
from google.cloud import translate_v2 as translate


def translate_consent(text, target_language):
    credentials, project = google.auth.default()
    translate_client = translate.Client(credentials=credentials)
    result = translate_client.translate(text, target_language=target_language)
    return result["translatedText"]
