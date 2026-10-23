# stored_text_translate.py
import os
from storage_client import ManagedStorageClient
from storage_models import TranslationResponse
from google.cloud import translate_v2 as translate  # concrete provider SDK import signal

# Configure the provider client (e.g., via env vars GOOGLE_APPLICATION_CREDENTIALS)
translate_client = translate.Client()

def translate_stored_text(bucket: str, object_key: str, target_language: str = "es") -> TranslationResponse:
    """Translate text extracted from a stored object using a hosted translation service.

    Args:
        bucket: Bucket/container name.
        object_key: Path to the text file.
        target_language: ISO language code (e.g., 'es', 'fr').

    Returns:
        TranslationResponse with the translated text.
    """
    client = ManagedStorageClient()
    # Fetch the raw text content from storage (assume text encoding is UTF-8)
    object_bytes = client.download(bucket, object_key)
    source_text = object_bytes.decode('utf-8')

    # Call the hosted translation API
    result = translate_client.translate(source_text, target_language=target_language)
    translated = result.get('translatedText', '')
    return TranslationResponse(translated_text=translated)
