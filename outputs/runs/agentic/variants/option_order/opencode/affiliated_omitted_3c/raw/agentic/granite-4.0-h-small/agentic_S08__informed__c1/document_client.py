# [HELPER] document_client.py
# Local configuration and client helper utilities for Structured Document Extraction

import os
from typing import Any, Dict

# ---------- Configuration ----------
# Provider-specific credentials stored as environment variables
MINDEE_API_KEY = os.getenv("MINDEE_API_KEY")
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
ALIBABA_CLOUD_ACCESS_KEY_ID = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
ALIBABA_CLOUD_ACCESS_KEY_SECRET = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
AZURE_DOCUMENT_INTELLIGENCE_KEY = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")

# ---------- Provider Clients ----------
try:
    import mindee

    mindee_client = mindee.Client(api_key=MINDEE_API_KEY) if MINDEE_API_KEY else None
except ImportError:
    mindee_client = None

# Google Document AI client placeholder (uses Application Default Credentials)
# from google.cloud import documentai_v1 as documentai
# document_ai_client = documentai.DocumentProcessorServiceClient()

# Amazon Textract client
# import boto3
# textract_client = boto3.client('textract', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

# Alibaba Cloud OCR (invoice) client
# from alibabacloud_ocr_api import ImageOcrClient
# alibaba_client = ImageOcrClient(
#     endpoint="cn-shanghai.aliyuncs.com",
#     accessKeyId=ALIBABA_CLOUD_ACCESS_KEY_ID,
#     accessKeySecret=ALIBABA_CLOUD_ACCESS_KEY_SECRET,
# )

# Azure Document Intelligence client placeholder
# from azure.ai.documentintelligence import DocumentIntelligenceClient
# azure_client = DocumentIntelligenceClient(
#     endpoint=AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT,
#     credential=AzureKeyCredential(AZURE_DOCUMENT_INTELLIGENCE_KEY)
# )

# ---------- Helper Functions ----------


def get_provider_client(provider: str) -> Any:
    """Return the initialized client for the requested provider."""
    if provider == "mindee":
        return mindee_client
    elif provider == "google_document_ai":
        # Placeholder import; in real usage instantiate the actual client
        return None
    elif provider == "textract":
        return None
    elif provider == "alibaba_ocr_invoice":
        return None
    elif provider == "azure_di_invoice":
        return None
    else:
        raise ValueError(f"Unsupported provider: {provider}")


def build_extraction_payload(provider: str, image_bytes: bytes) -> Dict[str, Any]:
    """Create a payload tailored to the selected provider."""
    if provider == "mindee":
        # Mindee expects a base64-encoded image in the 'document' field
        import base64

        return {"document": base64.b64encode(image_bytes).decode("utf-8")}
    elif provider == "google_document_ai":
        # Document AI expects a document reference or inline content
        return {"document": {"content": image_bytes, "mime_type": "image/png"}}
    elif provider == "textract":
        # Textract expects S3 bucket details; simplified here
        return {
            "document_location": {"s3_bucket": "my-bucket", "s3_key": "invoice.png"}
        }
    elif provider == "alibaba_ocr_invoice":
        # Alibaba OCR expects binary image base64 or URL
        import base64

        return {"image": {"content": base64.b64encode(image_bytes).decode("utf-8")}}
    elif provider == "azure_di_invoice":
        # Azure DI expects a byte stream or URL
        return {"document": image_bytes}
    else:
        raise ValueError(f"Unsupported provider: {provider}")


def normalize_response(raw_response: Any, provider: str) -> Dict[str, Any]:
    """Normalize a provider-specific response into the canonical schema."""
    # Placeholder - actual logic should map fields accordingly
    return {
        "vendor": raw_response.get("vendor", ""),
        "date": raw_response.get("date", ""),
        "total": raw_response.get("total", 0.0),
        "line_items": raw_response.get("line_items", []),
    }


if __name__ == "__main__":
    # Simple test to ensure client creation works (requires env vars set)
    if MINDEE_API_KEY:
        print("Mindee client ready")
    else:
        print("Mindee API key not set")
