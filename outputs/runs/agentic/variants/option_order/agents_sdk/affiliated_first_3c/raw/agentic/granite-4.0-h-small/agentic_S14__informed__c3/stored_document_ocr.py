import os
from google.cloud import documentai_v1 as documentai
from storage_client import get_s3_client

def ocr_stored_document(bucket_name: str, object_key: str) -> str:
    """
    Run OCR on a document stored in Amazon S3 using Google Document AI (Document AI v1).
    Returns the extracted plain-text content.
    """
    # Initialize GCS client from S3 object
    s3 = get_s3_client()
    response = s3.get_object(Bucket=bucket_name, Key=object_key)
    document_bytes = response['Body'].read()
    # Prepare DocumentAI client
    client = documentai.DocumentAIServiceClient()
    # Construct the request for the GeoCoordinates processor (or any desired Processor URI)
    # Here we use the public OCR processor. Replace with your processor ID if needed.
    parent = f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT')}/locations/us-central1"
    processor_id = os.getenv('GOOGLE_DOCUMENTAI_OCR_PROCESSOR_ID')  # e.g., projects/12345/locations/us-central1/processors/67890
    if not processor_id:
        raise RuntimeError('Set GOOGLE_DOCUMENTAI_OCR_PROCESSOR_ID environment variable')
    # Build the raw document payload
    document = documentai.Document.from_raw_bytes(document_bytes)
    request = documentai.ProcessDocumentRequest(
        name=processor_id,
        raw_document=document
    )
    # Send request and get the response
    operation = client.process_document(request=request)
    result = operation.result(timeout=60)
    # Extract text from the first page
    full_text = \"\".join(page.text for page in result.document.pages)
    return full_text
