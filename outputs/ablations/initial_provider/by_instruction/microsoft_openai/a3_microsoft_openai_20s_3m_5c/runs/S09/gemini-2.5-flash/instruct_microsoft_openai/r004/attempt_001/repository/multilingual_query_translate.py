from google.cloud import translate_v2 as translate
import os

def translate_query(query: str, target_language: str = 'en') -> str:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS_PATH")
    translate_client = translate.Client()

    result = translate_client.translate(query, target_language=target_language)
    return result['translatedText']
