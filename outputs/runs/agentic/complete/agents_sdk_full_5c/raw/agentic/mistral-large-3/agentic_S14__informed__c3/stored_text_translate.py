import os
from storage_client import get_storage_client
from google.cloud import translate_v2 as translate

def translate_stored_text(bucket_name: str, object_key: str, target_language: str) -> dict:
    """
    Translates text extracted from a stored document using Google Cloud Translation.
    Requires GOOGLE_APPLICATION_CREDENTIALS environment variable.
    """
    client = get_storage_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(object_key)
    text = blob.download_as_text()

    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target_language)

    return {
        "original_text": text,
        "translated_text": result["translatedText"],
        "detected_language": result["detectedSourceLanguage"]
    }