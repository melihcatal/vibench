import json
import time

from storage_client import get_s3_client, get_textract_client
from storage_models import StoredDocumentOcrRequest, StoredDocumentOcrResponse

def run_ocr_on_stored_document(
    request: StoredDocumentOcrRequest,
) -> StoredDocumentOcrResponse:
    """Runs OCR on a stored document object using AWS Textract."""
    textract_client = get_textract_client()
    s3_client = get_s3_client()

    # Start asynchronous detection of text
    response = textract_client.start_document_text_detection(
        DocumentLocation={
            'S3Object': {
                'Bucket': request.bucket_name,
                'Name': request.object_key
            }
        }
    )
    job_id = response['JobId']

    print(f"Started Textract job with ID: {job_id}")

    # Poll for job completion (simplified, in a real scenario use SNS/SQS)
    status = 'IN_PROGRESS'
    while status == 'IN_PROGRESS':
        time.sleep(5)  # Wait for 5 seconds before polling again
        job_status_response = textract_client.get_document_text_detection(
            JobId=job_id
        )
        status = job_status_response['JobStatus']
        print(f"Textract job {job_id} status: {status}")

    if status == 'SUCCEEDED':
        extracted_text = []
        pages = []
        next_token = None

        while True:
            if next_token:
                result_response = textract_client.get_document_text_detection(
                    JobId=job_id,
                    NextToken=next_token
                )
            else:
                result_response = textract_client.get_document_text_detection(
                    JobId=job_id
                )

            blocks = result_response['Blocks']
            for block in blocks:
                if block['BlockType'] == 'LINE':
                    extracted_text.append(block['Text'])
            
            if 'NextToken' in result_response:
                next_token = result_response['NextToken']
            else:
                break

        return StoredDocumentOcrResponse(
            object_key=request.object_key,
            extracted_text="\n".join(extracted_text),
            job_id=job_id,
        )
    else:
        raise RuntimeError(f"Textract job {job_id} failed with status: {status}")
