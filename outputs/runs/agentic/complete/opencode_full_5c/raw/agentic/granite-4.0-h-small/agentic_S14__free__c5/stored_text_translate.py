# stored_text_translate.py
# [LATER-STEP] Translates text extracted from a stored document using a managed translation service

import json
from google.cloud import storage, translate_v2 as translate
from storage_client import ManagedStorageClient
from storage_models import ObjectMetadataResponse


def translate_stored_text(
    bucket_name: str, blob_name: str, target_language: str = "en"
) -> json:
    """Translate the text content of a stored document/object.

    Args:
        bucket_name (str): Bucket containing the text file.
        blob_name (str): Object/key of the text document.
        target_language (str): ISO language code for translation (default "en").

    Returns:
        JSON string: Translated text wrapped in a structured response.
    """
    client = ManagedStorageClient().get_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    # Retrieve the original text (UTF-8 assumed)
    original_text = blob.download_as_text()

    # Initialize Translation API client
    translator = translate.Client(credentials=client._credentials)

    # Perform translation
    result = translator.translate(original_text, target_language=target_language)

    # Return structured JSON
    return json.dumps(
        {
            "original_text": result["input"],
            "translated_text": result["translatedText"],
            "detected_source_language": result["sourceLanguageCode"],
            "target_language": target_language,
        },
        indent=2,
    )
