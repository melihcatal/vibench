import os
import datetime
from storage_client import get_managed_storage_client
from google.cloud import documentai_v1 as documentai

def ocr_stored_document(bucket_name, object_key):
    """Run OCR on a stored document using Google Document AI.

    Returns extracted text and page info.
    """
    # Configure connection to Google Cloud services (uses GOOGLE_APPLICATION_CREDENTIALS env var)
    client = documentai.DocumentAIServiceClient()
    # Build the document reference to the object in Object Storage (placeholder - assumes a publicly accessible URL)
    document_uri = f"gs://{bucket_name}/{object_key}"
    # Construct the request payload
    gcs_source = documentai.types.GcsSource(uri=document_uri)
    input_config = documentai.types.InputConfig(gcs_source=gcs_source)
    \\ Configure the processor (select a processor ID from your GCP console)
    processor_name = "projects/PROJECT/locations/us/processors/PROCESSOR_ID"
    request = documentai.types.DocumentAIRequest(name=processor_name, input_config=input_config)
    \\ Send the OCR request
    response = client.process_document(request=request)
    document = response.document
    pages = []
    for page in document.pages:
        # Extract blocks (words, paragraphs) from each page
        lines = [
            block.text for field in page.fields.values() for block in field.text_anchor.content.splitlines()
        ]
        pages.append({'text': '\\n'.join(lines)})
    return {'pages': pages}
