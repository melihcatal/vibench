import os
import json
from storage_client import get_s3_client
from storage_models import validate_bucket_and_key, normalize_object_info

def stored_document_ocr(bucket: str, key: str, ocr_service: str = 'google-documentai'):
    """Extract text from a stored document using Google Document AI.

    bucket: S3 bucket containing the PDF/image file
    key: object key (path) to the document file
    ocr_service: identifier for the OCR provider (currently only 'google-documentai')
    Returns the extracted text as a plain string.
    """
    # 1. Download the object as bytes
    s3 = get_s3_client()
    validate_bucket_and_key(bucket, key)
    obj_response = s3.get_object(Bucket=bucket, Key=key)
    document_bytes = obj_response['Body'].read()

    # 2. Call Google Document AI (hosted endpoint) via its SDK
    #    Minimal placeholder using google-cloud-documentai.
    from google.cloud import documentai_v1 as documentai
    client = documentai.DocumentProcessorServiceClient()
    # Environment variable GOOGLE_APPLICATION_CREDENTIALS points to JSON key
    # Construct the processor name: projects/{PROJECT_ID}/locations/{LOCATION}/processors/{PROCESSOR_ID}
    processor_id = os.getenv('GOOGLE_DOCUMENTAI_PROCESSOR_ID')
    if not processor_id:
        raise RuntimeError('Set GOOGLE_DOCUMENTAI_PROCESSOR_ID environment variable')
    name = f'projects/{os.getenv(‘GOOGLE_CLOUD_PROJECT’)}/locations/us-central1/processors/{processor_id}'

    # Prepare the request
    gcs_source = documentai.types.GcsSource(uri=f'gs://{bucket}/{key}')
    input_config = documentai.types.InputConfig(gcs_source=gcs_source)
    document = documentai.types.Document(content=document_bytes, mime_type='application/pdf')
    request = documentai.types.ProcessDocumentRequest(name=name, input_config=input_config)

    # Call the API
    response = client.process_document(request=request)
    # The response contains a document with pages and text annotations
    text = ''.join(page.text for page in response.document.pages)
    print(f'Extracted OCR text from s3://{bucket}/{key} (using {ocr_service})')
    return text
