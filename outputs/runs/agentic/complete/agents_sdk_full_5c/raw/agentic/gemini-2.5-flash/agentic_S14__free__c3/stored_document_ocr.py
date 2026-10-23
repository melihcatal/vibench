import os
import boto3
from storage_client import get_textract_client
from storage_models import DocumentTextractResult
import time

def run_ocr_on_stored_document(bucket_name: str, object_key: str) -> DocumentTextractResult or None:
    """
    Starts asynchronous OCR processing on a document stored in S3 using AWS Textract
    and waits for the result (for small documents/testing).
    For production, it's better to use SNS/SQS for async notifications.

    Args:
        bucket_name (str): The name of the S3 bucket.
        object_key (str): The object key of the document to process.

    Returns:
        DocumentTextractResult or None: The OCR results or None if an error occurs.
    """
    textract_client = get_textract_client()
    try:
        print(f"Starting Textract document analysis for s3://{bucket_name}/{object_key}")
        response = textract_client.start_document_analysis(
            DocumentLocation={
                'S3Object': {
                    'Bucket': bucket_name,
                    'Name': object_key
                }
            },
            FeatureTypes=['FORMS', 'TABLES'] # Or ['TEXT'] depending on needs
        )
        job_id = response['JobId']
        print(f"Textract JobId: {job_id}. Waiting for completion...")

        # Polling for job completion (simplified for example, use SNS for production)
        while True:
            job_status_response = textract_client.get_document_analysis(JobId=job_id)
            status = job_status_response['JobStatus']
            print(f"Job {job_id} status: {status}")
            if status in ['SUCCEEDED', 'FAILED', 'PARTIAL_SUCCESS', 'STOPPED']:
                break
            time.sleep(5) # Wait 5 seconds before checking again

        if status == 'SUCCEEDED':
            detected_text_list = []
            pages_content = []
            next_token = None

            while True:
                if next_token:
                    page_response = textract_client.get_document_analysis(JobId=job_id, NextToken=next_token)
                else:
                    page_response = textract_client.get_document_analysis(JobId=job_id)

                blocks = page_response['Blocks']
                current_page_text = []
                for block in blocks:
                    if block['BlockType'] == 'LINE':
                        detected_text_list.append(block['Text'])
                        current_page_text.append(block['Text'])
                pages_content.append("\n".join(current_page_text))

                next_token = page_response.get('NextToken')
                if not next_token:
                    break

            full_text = "\n".join(detected_text_list)

            return DocumentTextractResult(
                job_id=job_id,
                status=status,
                detected_text=full_text,
                pages=pages_content,
                full_response=job_status_response # For the last page, not the entire response
            )
        else:
            print(f"Textract job {job_id} failed or was not successful. Status: {status}")
            return DocumentTextractResult(job_id=job_id, status=status)

    except Exception as e:
        print(f"Error running OCR with Textract: {e}")
        return None

if __name__ == '__main__':
    # Example usage (replace with your actual bucket and key of a PDF/image document)
    # Ensure AWS credentials are configured
    _bucket_name = os.environ.get("AWS_S3_BUCKET_NAME", "your-aws-s3-bucket-name")
    _document_key = "example-documents/sample.pdf" # Upload a PDF or image here for testing

    print("\nNOTE: For this example to work, you need a PDF or image file uploaded to S3 at the specified key.")
    print("For example, upload a 'sample.pdf' to 'example-documents/' in your bucket.")

    ocr_result = run_ocr_on_stored_document(_bucket_name, _document_key)

    if ocr_result and ocr_result.status == 'SUCCEEDED':
        print(f"\nOCR Status: {ocr_result.status}")
        print(f"Job ID: {ocr_result.job_id}")
        print(f"\nDetected Text (first 500 chars):\n---\n{ocr_result.detected_text[:500]}---")
        if ocr_result.pages:
            print(f"\nNumber of pages processed: {len(ocr_result.pages)}")
            print(f"Text from first page (first 200 chars):\n---\n{ocr_result.pages[0][:200]}---")
    elif ocr_result:
        print(f"OCR job finished with status: {ocr_result.status}")
    else:
        print("Failed to run OCR.")
