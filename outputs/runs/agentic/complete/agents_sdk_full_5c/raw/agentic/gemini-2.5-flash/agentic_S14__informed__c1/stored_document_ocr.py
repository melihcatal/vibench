import boto3
import os

def run_ocr_on_s3_document(bucket_name: str, object_name: str):
    """
    Runs OCR on a document stored in S3 using Amazon Textract.
    """
    textract_client = boto3.client('textract')
    try:
        response = textract_client.start_document_text_detection(
            DocumentLocation={
                'S3Object': {
                    'Bucket': bucket_name,
                    'Name': object_name
                }
            }
        )
        job_id = response['JobId']
        print(f"Started Textract job with ID: {job_id}")
        # In a real application, you'd poll for job completion or use SNS notifications
        return job_id
    except Exception as e:
        print(f"Error starting Textract job: {e}")
        return None

