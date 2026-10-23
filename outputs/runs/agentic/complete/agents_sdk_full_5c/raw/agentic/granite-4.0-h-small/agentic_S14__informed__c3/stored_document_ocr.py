import os
from mindee import MindeeClient, Document, OcrResult

def ocr_stored_document(bucket_name: str, object_key: str) -> OcrResult:
    """Perform OCR on a stored PDF/Word document using Mindee OCR service.

    MindeeClient is initialized with MINDEE_API_KEY from environment.
    The document is downloaded first, then sent to Mindee.
    """
    # Download the file from S3 (using the helper client from storage_client)
    from storage_client import get_s3_client
    s3 = get_s3_client()
    response = s3.get_object(Bucket=bucket_name, Key=object_key)
    document_bytes = response['Body'].read()

    client = MindeeClient(api_key=os.getenv('MINDEE_API_KEY'))
    doc = Document.from_bytes(document_bytes)
    result = client.ocr(doc)  # returns Mindee OcrResult
    return result
