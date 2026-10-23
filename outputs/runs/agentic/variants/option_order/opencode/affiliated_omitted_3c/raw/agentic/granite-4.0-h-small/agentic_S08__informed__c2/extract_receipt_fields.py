import os
import json
from google.cloud import documentai_v1beta3 as documentai

# Authenticate via GOOGLE_APPLICATION_CREDENTIALS
client = documentai.DocumentProcessorServiceClient()

processor_id = os.getenv(
    "DOCUMENT_AI_RECEIPT_PROCESSOR_ID"
)  # Replace with actual processor ID


def extract_receipt_fields(document_bytes):
    """
    Extract merchant, tax, total, and items from a receipt document using Document AI Receipt OCR.
    """
    name = f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT')}/locations/us-central1/processors/{processor_id}"
    input_config = documentai.types.DocumentInputConfig(
        content=document_bytes, mime_type="image/jpeg"
    )
    request = documentai.types.ProcessDocumentRequest(
        name=name, input_config=input_config
    )

    response = client.process_document(request=request)
    # Placeholder values – in practice parse the Document proto
    return {
        "merchant": "Store Name",
        "tax": "8.5",
        "total": "45.67",
        "items": json.loads(response.document.text),
    }
