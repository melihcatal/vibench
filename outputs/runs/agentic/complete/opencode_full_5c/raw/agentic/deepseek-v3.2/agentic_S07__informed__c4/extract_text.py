import os
from typing import Optional, Dict, Any
from document_client import DocumentClient
from document_models import TextExtractionRequest, TextExtractionResponse


def extract_text(
    image_path: str, mime_type: Optional[str] = None
) -> TextExtractionResponse:
    """
    Extract plain text from a scanned document image using Google Document AI.
    """
    client = DocumentClient.get_documentai_client()

    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")

    with open(image_path, "rb") as f:
        image_content = f.read()

    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "default-project")
    location = os.environ.get("DOCUMENTAI_LOCATION", "us")
    processor_id = os.environ.get("DOCUMENTAI_PROCESSOR_ID", "ocr-processor")

    name = f"projects/{project_id}/locations/{location}/processors/{processor_id}"

    raw_document = {"content": image_content, "mime_type": mime_type or "image/jpeg"}

    request = {"name": name, "raw_document": raw_document}

    result = client.process_document(request=request)

    document = result.document
    text = document.text

    return TextExtractionResponse(
        text=text, raw_response=result, provider="google_documentai"
    )
