from google.cloud import translate_v2 as translate
from storage_client import StorageClient


def translate_stored_text(bucket: str, key: str, target_language: str) -> str:
    """Translate text extracted from a stored document using Google Cloud Translation."""
    client = translate.Client()
    
    # Download the text from IBM COS
    storage_client = StorageClient().get_client()
    response = storage_client.get_object(Bucket=bucket, Key=key)
    text = response["Body"].read().decode("utf-8")
    
    # Translate
    result = client.translate(text, target_language=target_language)
    return result["translatedText"]