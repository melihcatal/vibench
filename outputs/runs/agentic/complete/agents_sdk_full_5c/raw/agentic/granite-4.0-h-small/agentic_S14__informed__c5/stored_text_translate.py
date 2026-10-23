import os
from google.cloud import translate_v2 as translate

def translate_text_from_gcs(bucket_name, blob_name, target_lang='en', source_lang=None):
    """Translate text extracted from a stored document using Google Cloud Translation."
    client = translate.Client()
    # Download text (assume UTF-8)
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    text = blob.download_as_text()
    # Detect language automatically if not provided
    if not source_lang:
        result = client.detect_language(text)
        source_lang = result['language']
    translation = client.translate(text, target_language=target_lang, source_language=source_lang)
    return {
        "translated_text": translation['translatedText'],
        "source_language": translation['detectedSourceLanguage'],
        "target_language": target_lang
    }
