from google.cloud import translate_v2 as translate
from storage_client import get_storage_client, get_bucket_name


def translate_stored_text(object_name: str, target_language: str = "es") -> str:
    """
    Translate text extracted from a stored document using Google Cloud Translation API.
    
    Args:
        object_name: Name of the object in the bucket (assumed to contain text).
        target_language: Target language code (e.g., 'es' for Spanish).
        
    Returns:
        Translated text.
    """
    client = translate.Client()
    bucket_name = get_bucket_name()
    
    # Fetch the object content
    bucket = get_storage_client().bucket(bucket_name)
    blob = bucket.blob(object_name)
    text = blob.download_as_text()
    
    # Translate the text
    result = client.translate(text, target_language=target_language)
    
    return result["translatedText"]