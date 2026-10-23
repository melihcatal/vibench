# stored_document_ocr.py
import os
import base64
from google.cloud import documentai_v1 as documentai
from storage_client import get_client, bucket_name
from storage_models import normalize_object_name

SERVICE = "Google Document AI"


def ocr_document(object_name: str) -> dict:
    """Run OCR on a stored document (PDF or image) and return extracted text."""
    # Document AI client reuses same credentials loaded by google-auth
    client = documentai.DocumentProcessorServiceClient()
    # Construct the document detail object
    document = {
        "content": base64.b64encode(
            open(normalize_object_name(object_name), "rb").read()
        ).decode("utf-8"),
        "mime_type": "application/pdf",  # adjust as needed (pdf, image/png, etc.)
    }
    # Define the processor (you must know the processor_id for your project)
    processor_id = os.getenv("DOCUMENT_AI_PROCESSOR_ID")
    if not processor_id:
        raise RuntimeError(
            "Set DOCUMENT_AI_PROCESSOR_ID environment variable to your Document AI processor ID."
        )
    name = f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT')}/locations/us-central1/processors/{processor_id}"
    response = client.process_document(name=name, document=document)
    # Extract full text from the response
    full_text = "\n".join(page.full_text for page in response.document.pages)
    return {"text": full_text, "pages": len(response.document.pages)}
