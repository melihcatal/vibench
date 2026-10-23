import boto3
from storage_client import get_textract_client
from storage_models import OcrDocumentRequest, OcrDocumentResponse
import time # For polling, if using async Textract

# This example uses asynchronous Textract for potentially large documents.
# For smaller documents, detect_document_text could be used directly if
# the document fits within synchronous call limits.

def run_ocr_on_stored_document(request: OcrDocumentRequest) -> OcrDocumentResponse:
    """
    Runs OCR on a stored document object in AWS S3 using AWS Textract.
    This implementation uses `start_document_text_detection` for asynchronous processing.
    """
    textract_client = get_textract_client()

    try:
        # Start the asynchronous text detection job
        response = textract_client.start_document_text_detection(
            DocumentLocation={
                'S3Object': {
                    'Bucket': request.bucket_name,
                    'Name': request.object_key
                }
            }
        )
        job_id = response['JobId']
        
        # In a real application, you'd typically use SNS/SQS for job completion notification.
        # For this example, we'll implement a basic polling mechanism for demonstration.
        
        status = "IN_PROGRESS"
        extracted_text_parts = []
        timeout_seconds = 600 # 10 minutes timeout
        start_time = time.time()

        while status == "IN_PROGRESS" and (time.time() - start_time < timeout_seconds):
            time.sleep(5) # Wait for 5 seconds before polling again
            job_response = textract_client.get_document_text_detection(JobId=job_id)
            status = job_response['JobStatus']

        if status == "SUCCEEDED":
            pages = []
            next_token = None
            while True:
                if next_token:
                    page_response = textract_client.get_document_text_detection(JobId=job_id, NextToken=next_token)
                else:
                    page_response = job_response # Use the initial response for the first page
                
                for block in page_response['Blocks']:
                    if block['BlockType'] == 'LINE':
                        extracted_text_parts.append(block['Text'])
                
                next_token = page_response.get('NextToken')
                if not next_token:
                    break
            
            return OcrDocumentResponse(
                success=True,
                job_id=job_id,
                extracted_text="\n".join(extracted_text_parts),
                message=f"OCR job {job_id} succeeded."
            )
        elif status == "FAILED":
            return OcrDocumentResponse(
                success=False,
                job_id=job_id,
                message=f"OCR job {job_id} failed: {job_response.get('StatusMessage', 'Unknown error')}"
            )
        else: # TIMED_OUT or other unexpected status
            return OcrDocumentResponse(
                success=False,
                job_id=job_id,
                message=f"OCR job {job_id} did not complete in time or had an unexpected status: {status}"
            )

    except textract_client.exceptions.InvalidS3ObjectException as e:
        return OcrDocumentResponse(success=False, message=f"Invalid S3 object specified: {e}")
    except textract_client.exceptions.InvalidParameterException as e:
        return OcrDocumentResponse(success=False, message=f"Invalid parameter for Textract: {e}")
    except Exception as e:
        return OcrDocumentResponse(success=False, message=f"An unexpected error occurred during OCR: {e}")

