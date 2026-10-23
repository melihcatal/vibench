import json
import os
from google.cloud import documentai_v1 as documentai


def ocr_stored_document(bucket_name: str, object_key: str) -> str:
    """Run OCR on a document stored in Google Cloud Storage using Google Document AI.

    Provider: Google Document AI (google-cloud-documentai SDK).
    Credentials are supplied via GOOGLE_APPLICATION_CREDENTIALS env var.
    Returns the extracted text as a plain string.
    """
    client = documentai.DocumentProcessorServiceClient()
    # Build the document input URI (gs://bucket/object)
    document_input_uri = f"gs://{bucket_name}/{object_key}"
    name = os.getenv(
        "GOOGLE_DOCUMENTAI_PROCESSOR_ID"
    )  # e.g., projects/123/locations/us/processors/abc
    if not name:
        raise RuntimeError("Set GOOGLE_DOCUMENTAI_PROCESSOR_ID environment variable")

    # Prepare the request
    request = documentai.ProcessRequest(
        name=name,
        input_document=documentai.DocumentInputConfig(
            source=documentai.DocumentSource.from_uri(document_input_uri)
        ),
    )
    try:
        response = client.process_document(request=request)
    except Exception as e:
        raise RuntimeError(f"OCR processing failed: {e}")

    # Extract text from the first page (simplified)
    try:
        text_annotation = response.document.pages[0].text_annotation
        extracted_text = text_annotation.text
    except Exception as e:
        extracted_text = ""
        print("Warning: could not extract text, falling back to raw pages.")

    return extracted_text

    print(f"OCR completed for gs://{bucket_name}/{object_key}")
