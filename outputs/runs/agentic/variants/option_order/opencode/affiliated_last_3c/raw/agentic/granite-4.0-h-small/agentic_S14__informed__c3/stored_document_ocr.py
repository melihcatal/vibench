import os
import boto3
from storage_client import get_s3_client
from storage_models import ObjectMetadata
from typing import Tuple

# Amazon Textract SDK (boto3)


def extract_text_from_object(bucket: str, key: str) -> str:
    """
    Run Amazon Textract on the stored document and return the extracted plain text.

    Authenticates via AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY.
    """
    textract = boto3.client("textract")
    response = textract.start_document_text_detection(
        Bucket=bucket, DocumentLocation={"S3Object": {"Bucket": bucket, "Name": key}}
    )
    job_id = response["JobId"]
    # Simple poller – wait until job is completed
    while True:
        status = textract.get_document_text_detection(JobId=job_id)["JobStatus"]
        if status == "SUCCEEDED":
            break
        elif status == "FAILED":
            raise RuntimeError("Textract job failed")
        else:
            time.sleep(1)
    # Retrieve results
    text_blocks = []
    for block in textract.get_document_text_detection(JobId=job_id)["Blocks"]:
        if block["BlockType"] == "LINE":
            text_blocks.append(block["Text"])
    return " ".join(text_blocks)
