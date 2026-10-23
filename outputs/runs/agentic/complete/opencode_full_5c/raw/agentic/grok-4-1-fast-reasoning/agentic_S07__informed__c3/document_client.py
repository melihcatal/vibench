import os
from typing import Dict


def load_image_bytes(image_path: str) -> bytes:
    with open(image_path, "rb") as f:
        return f.read()


def get_mime_type(image_path: str) -> str:
    ext = os.path.splitext(image_path)[1].lower()
    mime_map = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".tiff": "image/tiff",
        ".pdf": "application/pdf",
    }
    return mime_map.get(ext, "application/octet-stream")


def create_azure_di_client():
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.documentintelligence import DocumentIntelligenceClient

    endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")
    return DocumentIntelligenceClient(endpoint, AzureKeyCredential(key))


def create_textract_client():
    import boto3

    return boto3.client("textract")


def create_google_dai_client():
    from google.cloud import documentai_v1 as documentai

    return documentai.DocumentProcessorServiceClient()


def get_google_dai_processor_name():
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_DOCUMENTAI_LOCATION", "us")
    processor_id = os.getenv("GOOGLE_DOCUMENTAI_PROCESSOR_ID")
    return f"projects/{project_id}/locations/{location}/processors/{processor_id}"
