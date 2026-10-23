import os
import boto3
import logging
from botocore.exceptions import ClientError

# Provider: Amazon Textract
# SDK: boto3

def run_ocr_on_stored_document(bucket_name: str, document_key: str) -> str | None:
    """
    Performs synchronous OCR on a document stored in S3 using Amazon Textract.

    :param bucket_name: The S3 bucket where the document is stored.
    :param document_key: The key (path) of the document in the S3 bucket.
    :return: Extracted text as a single string, or None on failure.
    """
    textract_client = boto3.client(
        "textract",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
    )

    try:
        response = textract_client.detect_document_text(
            Document={"S3Object": {"Bucket": bucket_name, "Name": document_key}}
        )
        
        blocks = response.get("Blocks", [])
        extracted_text = []
        for block in blocks:
            if block["BlockType"] == "LINE":
                extracted_text.append(block["Text"])
        
        return "\n".join(extracted_text)

    except ClientError as e:
        logging.error(f"Error processing s3://{bucket_name}/{document_key} with Textract: {e}")
        return None
