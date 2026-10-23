# stored_document_ocr.py
# Run OCR on a stored document object using Amazon Textract (example)

import os
import boto3
from storage_client import get_s3_client
from storage_models import ObjectMetadata
from typing import Any, Dict


def ocr_stored_document(bucket: str, key: str) -> Dict[str, Any]:
    """Perform OCR on the document stored at s3://{bucket}/{key} and return results."""
    textract = boto3.client(
        "textract",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
    )
    try:
        response = textract.start_document_text_detection(
            DocumentLocation={"S3Object": {"Bucket": bucket, "Name": key}}
        )
        # The Call is asynchronous; for simplicity we poll until completion.
        while True:
            status = textract.get_document_text_detection(JobId=response["JobId"])[
                "JobStatus"
            ]
            if status == "SUCCEEDED":
                break
            elif status == "FAILED":
                raise RuntimeError(f"OCR job failed for s3://{bucket}/{key}")
    except Exception as exc:
        raise RuntimeError(f"OCR extraction error: {exc}") from exc

    # Retrieve and return OCR blocks
    result = textract.get_document_text_detection(JobId=response["JobId"])["Blocks"]
    return result  # dictionary-like structure containing words, lines, etc.


# Example usage:
# ocr_result = ocr_stored_document("my-bucket", "docs/report.pdf")
# print(ocr_result)
