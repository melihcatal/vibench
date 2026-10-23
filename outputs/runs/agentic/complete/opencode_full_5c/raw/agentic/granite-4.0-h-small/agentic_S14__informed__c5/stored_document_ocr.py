import os
from storage_client import (
    get_gcloud_storage_client,
    get_s3_client,
    get_azure_blob_client,
    get_oss_client,
    get_cos_client,
)
from storage_models import OCRDocument
from google.cloud import documentai_v1 as documentai
from typing import Optional

# Example: set ENV var PROVIDER to 's3', 'gcs', 'azure', 'oss', or 'cos' to select storage provider for the document file
# OCR is performed via Google Document AI (service=Google Document AI)


def ocr_stored_document(**kwargs):
    """
    Run OCR on a stored document object and return extracted plain text.
    Args (kwargs):
      bucket_name: storage bucket/container
      object_key: path/key of the document object
      provider: select storage provider (same set as other helpers)
    Returns OCRDocument with .text field.
    """
    provider = os.getenv("PROVIDER")
    if not provider:
        raise ValueError("ENV var PROVIDER must be set")
    bucket = kwargs["bucket_name"]
    key = kwargs["object_key"]

    # Load the raw document bytes from the selected storage
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

    # Google Document AI endpoint & region
    endpoint = os.getenv(
        "GOOGLE_DOCUMENTAI_ENDPOINT", "https://documentai.googleapis.com/v1"
    )
    processor_id = os.getenv(
        "GOOGLE_DOCUMENTAI_PROCESSOR_ID"
    )  # e.g., 'projects/123/locations/us/processors/abc'
    if not processor_id:
        raise ValueError("Set GOOGLE_DOCUMENTAI_PROCESSOR_ID env var")

    client = documentai.DocumentProcessorServiceClient()
    name = f"{endpoint}/projects/{processor_id}"
    raw_document = documentai.RawDocument(
        content=document_bytes, mime_type="application/pdf"
    )
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)
    result = client.process_document(request=request)

    # Extract full text (DocumentAI returns a structure; we just concatenate)
    text_parts = []
    for page in result.document.pages:
        text_parts.append(page.text)
    extracted_text = "\n".join(text_parts)

    return OCRDocument(text=extracted_text)
