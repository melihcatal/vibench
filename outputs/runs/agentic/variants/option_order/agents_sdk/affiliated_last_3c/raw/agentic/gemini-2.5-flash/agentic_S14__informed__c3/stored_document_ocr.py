import os
import boto3

def start_textract_document_analysis(bucket_name: str, object_key: str) -> str:
    """
    Starts an asynchronous document analysis job on a stored document object in Amazon S3
    using Amazon Textract.

    Args:
        bucket_name (str): The name of the S3 bucket where the document is stored.
        object_key (str): The key (path) of the document object in the bucket.

    Returns:
        str: The JobId of the started Textract analysis job.
    """
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    aws_region = os.environ.get("AWS_REGION", "us-east-1")

    if not aws_access_key_id or not aws_secret_access_key:
        raise ValueError("AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY must be set in environment variables.")

    textract_client = boto3.client(
        "textract",
        region_name=aws_region,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )

    response = textract_client.start_document_text_detection(
        DocumentLocation={
            'S3Object': {
                'Bucket': bucket_name,
                'Name': object_key
            }
        }
    )
    return response['JobId']
