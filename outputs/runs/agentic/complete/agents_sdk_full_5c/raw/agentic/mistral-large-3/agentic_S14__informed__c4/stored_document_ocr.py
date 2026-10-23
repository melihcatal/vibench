from google.cloud import documentai_v1 as documentai
from storage_client import StorageClient
import os


def run_ocr_on_stored_document(bucket: str, key: str, mime_type: str) -> str:
    """Run OCR on a stored document using Google Document AI."""
    client = documentai.DocumentProcessorServiceClient()
    processor_name = os.getenv("GOOGLE_DOCUMENT_AI_PROCESSOR_NAME")
    
    # Download the document from IBM COS
    storage_client = StorageClient().get_client()
    response = storage_client.get_object(Bucket=bucket, Key=key)
    document_content = response["Body"].read()
    
    # Process with Document AI
    request = {
        "name": processor_name,
        "raw_document": {
            "content": document_content,
            "mime_type": mime_type,
        },
    }
    result = client.process_document(request=request)
    return result.document.text