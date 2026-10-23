import os
from typing import Optional
from google.cloud import vision, documentai, translate_v2 as translate, language_v1
from google.oauth2 import service_account

# Configuration
GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT", "your-project-id")
GOOGLE_CLOUD_LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us")
DOCUMENT_AI_PROCESSOR_ID = os.getenv("DOCUMENT_AI_PROCESSOR_ID", "your-processor-id")
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# Client instances
_vision_client = None
_documentai_client = None
_translate_client = None
_language_client = None


def get_vision_client() -> vision.ImageAnnotatorClient:
    """Get or create Google Cloud Vision client."""
    global _vision_client
    if _vision_client is None:
        if GOOGLE_APPLICATION_CREDENTIALS:
            credentials = service_account.Credentials.from_service_account_file(
                GOOGLE_APPLICATION_CREDENTIALS
            )
            _vision_client = vision.ImageAnnotatorClient(credentials=credentials)
        else:
            _vision_client = vision.ImageAnnotatorClient()
    return _vision_client


def get_documentai_client() -> documentai.DocumentProcessorServiceClient:
    """Get or create Google Cloud Document AI client."""
    global _documentai_client
    if _documentai_client is None:
        if GOOGLE_APPLICATION_CREDENTIALS:
            credentials = service_account.Credentials.from_service_account_file(
                GOOGLE_APPLICATION_CREDENTIALS
            )
            _documentai_client = documentai.DocumentProcessorServiceClient(
                credentials=credentials
            )
        else:
            _documentai_client = documentai.DocumentProcessorServiceClient()
    return _documentai_client


def get_processor_name() -> str:
    """Get the full processor name for Document AI."""
    return f"projects/{GOOGLE_CLOUD_PROJECT}/locations/{GOOGLE_CLOUD_LOCATION}/processors/{DOCUMENT_AI_PROCESSOR_ID}"


def load_image_as_base64(image_path: str) -> str:
    """Load an image file and encode it as base64."""
    import base64

    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def validate_image_path(image_path: str) -> bool:
    """Validate that an image path exists and is readable."""
    return os.path.exists(image_path) and os.path.isfile(image_path)


def get_translate_client() -> translate.Client:
    """Get or create Google Cloud Translation client."""
    global _translate_client
    if _translate_client is None:
        if GOOGLE_APPLICATION_CREDENTIALS:
            credentials = service_account.Credentials.from_service_account_file(
                GOOGLE_APPLICATION_CREDENTIALS
            )
            _translate_client = translate.Client(credentials=credentials)
        else:
            _translate_client = translate.Client()
    return _translate_client


def get_language_client() -> language_v1.LanguageServiceClient:
    """Get or create Google Cloud Natural Language client."""
    global _language_client
    if _language_client is None:
        if GOOGLE_APPLICATION_CREDENTIALS:
            credentials = service_account.Credentials.from_service_account_file(
                GOOGLE_APPLICATION_CREDENTIALS
            )
            _language_client = language_v1.LanguageServiceClient(
                credentials=credentials
            )
        else:
            _language_client = language_v1.LanguageServiceClient()
    return _language_client


def get_supported_mime_types() -> list:
    """Get list of supported MIME types for document processing."""
    return [
        "image/jpeg",
        "image/png",
        "image/tiff",
        "image/bmp",
        "image/webp",
        "application/pdf",
        "image/gif",
    ]
