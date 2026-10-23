import os
from storage_client import (
    get_s3_client,
    get_gcloud_storage_client,
    get_azure_blob_client,
    get_b2_client,
    get_oss_client,
    get_cos_client,
)
from storage_models import TranslatedText
from google.cloud import translate_v2 as translate
from typing import Optional

# Provider selection via PROVIDER env var (same choices as other helpers)


def translate_stored_text(**kwargs):
    """
    Extract text from a stored document then translate it to a target language.
    Args (kwargs):
      bucket_name: storage bucket/container
      object_key: path/key of the document object
      provider: storage provider selector
      target_language: ISO language code (e.g., 'es', 'fr')
    Returns TranslatedText with .translated field.
    """
    provider = os.getenv("PROVIDER")
    if not provider:
        raise ValueError("ENV var PROVIDER must be set")
    bucket = kwargs["bucket_name"]
    key = kwargs["object_key"]
    target = kwargs["target_language"]

    # Load raw bytes from chosen storage (reuse logic from ocr_stored_document)
    if provider == "s3":
        client = get_s3_client()
        response = client.get_object(Bucket=bucket, Key=key)
        document_bytes = response["Body"].read()
    elif provider == "gcs":
        client = get_gcloud_storage_client()
        blob = client.bucket(bucket).blob(key)
        document_bytes = blob.download_as_bytes()
    elif provider == "azure":
        client = get_azure_blob_client()
        blob_service_client = client.get_blob_service_client()
        container_client = blob_service_client.get_container_client(bucket)
        blob_client = container_client.get_blob_client(key)
        document_bytes = blob_client.download_blob().readall()
    elif provider == "oss":
        client = get_oss_client()
        document_bytes = client.get_object(key).content
    elif provider == "cos":
        client = get_cos_client()
        document_bytes = client.get_object(bucket, key).content
    else:
        raise ValueError(f"Unknown provider {provider}")

    # Use Google Cloud Translation (service=Google Cloud Translation)
    client = translate.Client()
    result = client.translate(
        document_bytes, target_language=target, mime_type="text/plain"
    )
    # result['translatedText'] holds the translation
    return TranslatedText(translated=result["translatedText"])
