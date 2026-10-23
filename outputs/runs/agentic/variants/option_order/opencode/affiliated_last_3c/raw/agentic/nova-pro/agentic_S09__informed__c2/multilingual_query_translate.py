import os
from google.cloud import translate_v2 as translate


def translate_query(query, target_language):
    client = translate.Client(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
    result = client.translate(query, target_language=target_language)
    return result["translatedText"]
