import os
from google.cloud import translate_v2 as translate
from dotenv import load_dotenv

load_dotenv()


def translate_query(query: str, target_language: str = "en") -> str:
    """
    Translate a query before multilingual embedding search using Google Cloud Translation.
    Assumes GOOGLE_APPLICATION_CREDENTIALS environment variable is set.
    """
    translate_client = translate.Client()

    result = translate_client.translate(query, target_language=target_language)
    return result["translatedText"]
