import os
import datetime
from storage_client import get_managed_storage_client
from google.cloud import translate_v2 as translate


def translate_text_from_object(bucket_name, object_key, target_language="es"):
    """Translate text extracted from a stored document using Google Translate.

    Returns the translated text.
    """
    client = translate.Client()
    # Retrieve the object content (placeholder implementation)
    cos = get_managed_storage_client()
    blob = cos.get_object(Bucket=bucket_name, Key=object_key)
    original_text = blob["Body"].read().decode("utf-8")
    result = client.translate(original_text, target_language=target_language)
    return result["translatedText"]
