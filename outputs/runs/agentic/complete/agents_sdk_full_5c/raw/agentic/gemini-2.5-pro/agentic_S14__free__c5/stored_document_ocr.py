import os
import boto3
from botocore.exceptions import ClientError
from storage_client import get_aws_region

def run_ocr_on_s3_document(bucket_name: str, document_key: str) -> str | None:
    """
    Starts an asynchronous text detection job on a document stored in S3 using AWS Textract.

    Args:
        bucket_name: The S3 bucket where the document is stored.
        document_key: The key (path) of the document in the bucket.

    Returns:
        The JobId of the started Textract job, or None if an error occurred.
    """
    try:
        textract_client = boto3.client(
            "textract", 
            region_name=get_aws_region(),
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        )

        response = textract_client.start_document_text_detection(
            DocumentLocation={
                'S3Object': {
                    'Bucket': bucket_name,
                    'Name': document_key
                }
            }
        )
        
        job_id = response.get("JobId")
        print(f"Started AWS Textract job with ID: {job_id}")
        return job_id

    except ClientError as e:
        print(f"Error starting Textract job for s3://{bucket_name}/{document_key}: {e}")
        return None

# Example usage:
# if __name__ == '__main__':
#     S3_BUCKET = os.environ.get("AWS_S3_BUCKET")
#     # You would need a document (e.g., PDF, PNG) uploaded to this key
#     S3_KEY = "documents/sample-contract.pdf"
#     if S3_BUCKET:
#         job_id = run_ocr_on_s3_document(S3_BUCKET, S3_KEY)
#         if job_id:
#             print(f"To check status, use the AWS CLI or another script with this Job ID.")
#     else:
#         print("AWS_S3_BUCKET environment variable not set.")
