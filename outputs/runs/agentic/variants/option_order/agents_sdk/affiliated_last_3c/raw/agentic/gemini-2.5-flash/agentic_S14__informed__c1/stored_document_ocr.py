from storage_client import get_textract_client
from storage_models import OCRDocumentRequest, OCRDocumentResponse
from typing import List
import time

def run_ocr_on_stored_document(request: OCRDocumentRequest) -> OCRDocumentResponse:
    """Runs OCR on a stored document object in AWS S3 using Amazon Textract.

    Args:
        request: An OCRDocumentRequest containing the S3 bucket and object key.

    Returns:
        An OCRDocumentResponse with the extracted text and detected languages.
    """
    textract_client = get_textract_client()

    # Start asynchronous document analysis (for multi-page documents or large files)
    # For simplicity, we'll use start_document_text_detection, which is suitable for general text extraction.
    # For forms or tables, start_document_analysis would be used.
    response = textract_client.start_document_text_detection(
        DocumentLocation={
            'S3Object': {
                'Bucket': request.bucket_name,
                'Name': request.object_key
            }
        }
    )

    job_id = response['JobId']
    extracted_text_parts: List[str] = []
    detected_languages: List[str] = []

    print(f"Started Textract job with JobId: {job_id}")

    # Poll for job completion
    while True:
        job_status_response = textract_client.get_document_text_detection(
            JobId=job_id
        )
        status = job_status_response['JobStatus']
        print(f"Textract job status: {status}")

        if status == 'SUCCEEDED':
            break
        elif status == 'FAILED' or status == 'PARTIAL_SUCCESS':
            raise Exception(f"Textract job failed or partially succeeded: {job_status_response.get('StatusMessage')}")
        
        time.sleep(5) # Wait before polling again

    # Get results
    pages = textract_client.get_document_text_detection(JobId=job_id)
    
    for block in pages['Blocks']:
        if block['BlockType'] == 'WORD' or block['BlockType'] == 'LINE':
            if 'Text' in block:
                extracted_text_parts.append(block['Text'])
        # Textract does not directly return document-level language detection in this API.
        # One would typically use Amazon Comprehend for that on the extracted text.
        # For now, we will leave detected_languages as empty or infer from context if available.

    full_text = " ".join(extracted_text_parts)
    
    # Placeholder for language detection as Textract's core text detection doesn't provide it easily.
    # In a real scenario, you might pass the text to a language detection service like Amazon Comprehend.
    # For this example, we'll return an empty list or a default.
    
    return OCRDocumentResponse(extracted_text=full_text, detected_languages=[])
