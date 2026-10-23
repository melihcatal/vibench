import os
from google.cloud import documentai_v1 as documentai
from storage_client import get_storage_client
from typing import Optional

def ocr_stored_document(bucket_name: str, object_name: str) -> Optional[str]:
    """Extract text from a document stored in Google Cloud Storage using Google Document AI.

    Args:
        bucket_name (str): Bucket containing the document.
        object_name (str): Object (blob) name of the document.

    Returns:
        str: Extracted plain text or None if the operation fails.
    """
    client = get_storage_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(object_name)
    # Helper to download the document as bytes
    content = blob.download_as_bytes()
    if not content:
        print('Failed to download document')
        return None
    # Document AI client configuration (uses GOOGLE_APPLICATION_CREDENTIALS env var)
    processor_id = os.getenv('DOCUMENTAI_PROCESSOR_ID')
    if not processor_id:
        print('Missing DOCUMENTAI_PROCESSOR_ID environment variable')
        return None
    document = documentai.Document.from_bytes(content)
    # Assume a regional endpoint, e.g., us-central1
    endpoint = f'https://documentai.googleapis.com/v1/projects/{os.getenv("GOOGLE_CLOUD_PROJECT")}/locations/us-central1/processors/{processor_id}:batchProcess'
    request = documentai.BatchProcessRequest(name=endpoint, input_config={'document': {'content': content}})
    # The SDK call; raises on error
    try:
        response = documentai.DocumentProcessorServiceClient().batch_process_document(request=request)
    except Exception as e:
        print(f'OCR processing error: {e}')
        return None
    # Extract plain text from the first page
    try:
        text = response.output[0].document.pages[0].text
        return text.text if text else ''
    except Exception:
        return ''
