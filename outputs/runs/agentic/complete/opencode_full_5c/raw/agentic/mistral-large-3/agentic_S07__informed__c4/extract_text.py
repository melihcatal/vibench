from google.cloud import documentai_v1 as documentai
import os
from typing import Optional
from document_client import get_document_client
from document_models import DocumentTextResponse


def extract_text_from_image(
    image_path: str, mime_type: str = "image/png"
) -> DocumentTextResponse:
    """
    Extracts plain text from a scanned document image using Google Document AI.

    Args:
        image_path: Path to the document image file.
        mime_type: MIME type of the image (e.g., "image/png", "image/jpeg").

    Returns:
        DocumentTextResponse containing the extracted text and metadata.
    """
    client = get_document_client("google")
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    location = os.getenv("GOOGLE_DOCUMENT_AI_LOCATION", "us")
    processor_id = os.getenv("GOOGLE_DOCUMENT_AI_PROCESSOR_ID")

    if not all([project_id, processor_id]):
        raise ValueError(
            "Google Cloud project ID and processor ID must be set in environment variables."
        )

    processor_name = (
        f"projects/{project_id}/locations/{location}/processors/{processor_id}"
    )

    with open(image_path, "rb") as image_file:
        image_content = image_file.read()

    request = {
        "name": processor_name,
        "raw_document": {"content": image_content, "mime_type": mime_type},
    }

    result = client.process_document(request=request)
    document = result.document

    return DocumentTextResponse(
        text=document.text,
        pages=len(document.pages),
        language=document.language_code,
        provider="google_document_ai",
        model="pretrained-ocr-v2.0-2023-06-02",
    )
