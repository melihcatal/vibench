import os
from google.cloud import translate_v2 as translate
from database_models import Document


def translate_document_content(document: Document, target_language: str) -> Document:
    """
    Translates user-facing fields of a document using Google Cloud Translation API.
    """
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        raise EnvironmentError(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable not set."
        )

    translate_client = translate.Client()

    if "content" in document and isinstance(document["content"], str):
        result = translate_client.translate(
            document["content"], target_language=target_language
        )
        document["content"] = result["translatedText"]

    # Example for another field
    if "author" in document and isinstance(document["author"], str):
        result = translate_client.translate(
            document["author"], target_language=target_language
        )
        document["author"] = result["translatedText"]

    return document
