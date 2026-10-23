import os
import boto3
from storage_client import ManagedObjectStorageClient
from google.cloud import documentai_v1 as documentai


def ocr_stored_document(bucket: str, key: str) -> dict:
    """Extract text/OCR from a document stored in S3 and Google Document AI.

    Parameters:
        bucket (str): Bucket name.
        key (str): Object key/path.

    Returns:
        dict: Parsed OCR response with parsed text and layout.
    """
    # Load document content from S3
    client = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )
    response = client.get_object(Bucket=bucket, Key=key)
    document_bytes = response["Body"].read()

    # Use Google Document AI (PDF/IMAGE OCR)
    client_ocr = documentai.DocumentAIServiceClient()
    parent = "projects/12345/locations/us"
    document = documentai.Document(content=document_bytes, mime_type="application/pdf")
    request = documentai.BatchProcessRequest(parent=parent, documents=[document])
    result = client_ocr.batch_process_documents(request=request)
    # Simplify result to plain text and layout info
    return {
        "full_text": "Placeholder text extraction",  # Implementation needed
        "layout": [],  # Placeholder for layout data
    }
