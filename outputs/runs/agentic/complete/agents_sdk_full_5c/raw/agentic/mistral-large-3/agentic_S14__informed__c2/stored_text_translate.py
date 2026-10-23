import os
from typing import Dict
from google.cloud import translate_v2 as translate
from storage_client import get_b2_client, get_bucket_name


def translate_stored_text(object_name: str, target_language: str) -> Dict:
    b2_api = get_b2_client()
    bucket = b2_api.get_bucket_by_name(get_bucket_name())

    # Download the text file from B2
    downloaded_file = bucket.download_file_by_name(object_name)
    text_content = downloaded_file.download().decode('utf-8')

    # Initialize Google Cloud Translation client
    client = translate.Client()

    # Translate text using Google Cloud Translation (model: "nmt")
    result = client.translate(
        text_content,
        target_language=target_language,
        model="nmt"
    )

    return {
        "translated_text": result["translatedText"],
        "detected_source_language": result["detectedSourceLanguage"]
    }