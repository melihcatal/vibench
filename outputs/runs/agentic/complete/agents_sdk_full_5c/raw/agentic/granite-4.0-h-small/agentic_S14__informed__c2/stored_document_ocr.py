import os
from storage_client import create_aws_s3_client
from storage_models import S3HeadObjectResult, OCRResult
from google.cloud import documentai_v1 as documentai

def ocr_stored_document(bucket_name, object_key):
    """Extract text (OCR) from a document stored in S3 using Google Document AI.

    The document is first downloaded from S3, then uploaded to Document AI for processing.
    Returns an OCRResult containing the extracted plain text.
    """
    # 1. Download the object from S3
    client = create_aws_s3_client()
    download_response = client.get_object(Bucket=bucket_name, Key=object_key)
    document_bytes = download_response['Body'].read()

    # 2. Prepare Document AI request
    client_ai = documentai.DocumentProcessorServiceClient()
    # Construct the full processor name (example uses the default processor)
    processor_name = 'projects/your-project/locations/us-central1/processors/your-processor-id'
    document = documentai.Document.from_bytes(document_bytes)
    request = documentai.ProcessDocumentRequest(processor_name=processor_name, document=document)

    # 3. Call Document AI and collect plain text from the first page
    response = client_ai.process_document(request=request)
    # Extract plain text from the first page layout
    layout = response.document.pages[0].layout
    text = layout.text_anchor.content if layout.text_anchor else ''

    return OCRResult(text=text)
