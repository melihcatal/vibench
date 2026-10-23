import json
import os
from google.cloud import documentai_v1beta3 as documentai
from google.oauth2 import service_account

# Service identifier:
# Provider: Google Document AI

def extract_text_from_image(image_bytes: bytes) -> str:
    """Extract plain text from a scanned document image using Google Document AI.

    Args:
        image_bytes: binary image data (e.g., PNG, JPEG).

    Returns:
        Extracted plain text string.
    """
    # Load credentials from environment variable
    credentials = service_account.Credentials.from_service_account_file(
        os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))

    # Construct the Document AI processor (OCR) client
    processor = documentai.DocumentProcessorServiceClient()
    # For demo we use the default processor; replace with your processor ID
    processor_name = "projects/your-project/locations/us-central1/processors/ocr-processor"

    # Prepare the document payload
    document = documentai.Document.fromJson({"content": image_bytes, "mime_type": "image/jpeg"})

    # Request OCR
    response = processor.process_document(
        name=processor_name,
        raw_document=document,
    )

    # Retrieve recognized text
    text = response.document.text
    return text
