import os
import boto3
from storage_client import get_textract_client
from storage_models import OCRResult

def start_document_text_detection(bucket_name: str, object_name: str, sns_topic_arn: str = None, kms_key_id: str = None) -> OCRResult | None:
    """
    Starts an asynchronous job to detect text in a document stored in S3 using Amazon Textract.
    Requires permissions for Textract, S3, and optionally SNS and KMS.
    """
    textract_client = get_textract_client()
    
    try:
        document_location = {
            'S3Object': {
                'Bucket': bucket_name,
                'Name': object_name
            }
        }

        notification_channel = None
        if sns_topic_arn:
            notification_channel = {
                'SNSTopicArn': sns_topic_arn,
                'RoleArn': os.environ.get("AWS_SNS_ROLE_ARN") # Ensure this env var is set if using SNS
            }
        
        # Start text detection
        if notification_channel:
            response = textract_client.start_document_text_detection(
                DocumentLocation=document_location,
                NotificationChannel=notification_channel,
                KMSKeyId=kms_key_id
            )
        else:
            response = textract_client.start_document_text_detection(
                DocumentLocation=document_location,
                KMSKeyId=kms_key_id
            )

        job_id = response.get('JobId')
        print(f"Started Textract document text detection job with JobId: {job_id}")
        return OCRResult(job_id=job_id, status="IN_PROGRESS")

    except Exception as e:
        print(f"Error starting Textract job: {e}")
        return None

def get_document_text_detection_results(job_id: str) -> OCRResult | None:
    """
    Retrieves the results of a Textract document text detection job.
    """
    textract_client = get_textract_client()
    try:
        full_text = []
        pages = 0
        next_token = None

        while True:
            if next_token:
                response = textract_client.get_document_text_detection(JobId=job_id, NextToken=next_token)
            else:
                response = textract_client.get_document_text_detection(JobId=job_id)
            
            status = response.get('JobStatus')
            if status not in ['SUCCEEDED', 'FAILED', 'PARTIAL_SUCCESS']:
                return OCRResult(job_id=job_id, status=status)

            for block in response.get('Blocks', []):
                if block['BlockType'] == 'WORD':
                    full_text.append(block['Text'])
                elif block['BlockType'] == 'PAGE':
                    pages += 1
            
            next_token = response.get('NextToken')
            if not next_token:
                break

        return OCRResult(job_id=job_id, text_content=" ".join(full_text), pages=pages, status=status)

    except Exception as e:
        print(f"Error getting Textract job results: {e}")
        return None

if __name__ == '__main__':
    # Example usage (replace with actual values)
    bucket = os.environ.get("S3_BUCKET_NAME", "my-textract-bucket")
    object_key = os.environ.get("S3_DOCUMENT_KEY", "documents/sample.pdf")
    # SNS Topic ARN and AWS_SNS_ROLE_ARN environment variable are required for asynchronous processing
    sns_topic = os.environ.get("AWS_TEXTRACT_SNS_TOPIC_ARN")

    # To run this example, you would typically upload a PDF/image to S3 first.
    # For synchronous processing, you would use detect_document_text or analyze_document,
    # but for potentially large stored documents, asynchronous is preferred.
    # This example only starts the job; getting results requires polling or SNS notifications.
    
    print(f"Attempting to start Textract job for {bucket}/{object_key}")
    job_start_result = start_document_text_detection(bucket, object_key, sns_topic)
    if job_start_result and job_start_result.job_id:
        print(f"Textract job started successfully with ID: {job_start_result.job_id}")
        print("You would typically poll get_document_text_detection_results or wait for SNS notification.")
        # For demonstration, let's pretend to get results (in a real scenario, this would be later)
        # For simplicity in this direct script, we won't poll here. 
        # A separate process or lambda would typically handle result retrieval.
    else:
        print("Failed to start Textract job.")
