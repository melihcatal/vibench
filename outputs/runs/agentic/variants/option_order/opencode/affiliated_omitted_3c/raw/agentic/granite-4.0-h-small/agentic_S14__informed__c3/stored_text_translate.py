# stored_text_translate.py
import os
from google.cloud import translate_v2 as translate
from storage_client import get_client, bucket_name
from storage_models import normalize_object_name

SERVICE = "Google Cloud Translation"


def translate_text(object_name: str, target_lang: str = "en") -> str:
    """Extract text from a stored document, translate it, and return the translated string."""
    # Reuse storage client to access the file
    client = get_client()
    bucket = client.bucket(bucket_name())
    blob = bucket.blob(normalize_object_name(object_name))
    content = blob.download_as_text()
    translator = translate.Client()
    result = translator.translate(content, target_language=target_lang)
    return result["translatedText"]
