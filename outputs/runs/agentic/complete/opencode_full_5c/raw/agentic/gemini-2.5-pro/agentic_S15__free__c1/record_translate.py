import os
from google.cloud import translate_v2 as translate
from database_models import Document


def record_translate(document: Document, target_language: str = "es") -> str:
    """
    Translates the document's content to a target language using Google Cloud Translation API.
    """
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.environ.get(
        "GOOGLE_APPLICATION_CREDENTIALS"
    )
    translate_client = translate.Client()

    if not isinstance(document.content, str):
        return ""

    result = translate_client.translate(
        document.content, target_language=target_language
    )
    return result["translatedText"]
