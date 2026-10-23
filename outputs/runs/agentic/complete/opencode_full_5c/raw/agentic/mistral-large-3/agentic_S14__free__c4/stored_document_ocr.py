import os
from typing import Optional

import boto3
from botocore.exceptions import ClientError


def stored_document_ocr(
    bucket: str, key: str, output_bucket: Optional[str] = None
) -> dict:
    """
    Runs Amazon Textract OCR on a stored document object in S3.

    Args:
        bucket: Name of the S3 bucket containing the document.
        key: Object key (path) of the document in the bucket.
        output_bucket: Optional S3 bucket to store OCR results (default: same as input bucket).

    Returns:
        dict: Textract job response containing job ID and status.
    """
    textract = boto3.client(
        "textract",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-1"),
    )

    output_bucket = output_bucket or bucket

    try:
        response = textract.start_document_text_detection(
            DocumentLocation={"S3Object": {"Bucket": bucket, "Name": key}},
            OutputConfig={"S3Bucket": output_bucket},
        )
        return {
            "job_id": response["JobId"],
            "status": "STARTED",
            "output_location": f"s3://{output_bucket}/{response['JobId']}",
        }
    except ClientError as e:
        raise Exception(f"Failed to start Textract OCR job: {e}")
