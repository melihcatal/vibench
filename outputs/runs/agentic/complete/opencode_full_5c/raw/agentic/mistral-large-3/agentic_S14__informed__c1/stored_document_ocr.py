import os
from typing import BinaryIO

import boto3
from botocore.exceptions import ClientError
from PIL import Image
import io

from storage_client import get_storage_client


def run_ocr_on_stored_document(
    bucket_name: str,
    object_key: str,
    output_bucket: str = None,
    output_key: str = None,
) -> dict:
    """
    Runs Amazon Textract OCR on a document stored in Amazon S3.

    Args:
        bucket_name: Name of the S3 bucket containing the document.
        object_key: Key of the document in the bucket.
        output_bucket: Optional bucket to store results. Defaults to input bucket.
        output_key: Optional key for storing results. Defaults to <object_key>.json.

    Returns:
        Dictionary containing OCR results from Amazon Textract.
    """
    textract_client = boto3.client("textract")
    s3_client = get_storage_client()

    if not output_bucket:
        output_bucket = bucket_name
    if not output_key:
        output_key = f"{object_key}.ocr.json"

    try:
        # Start Textract OCR job
        response = textract_client.start_document_text_detection(
            DocumentLocation={
                "S3Object": {
                    "Bucket": bucket_name,
                    "Name": object_key,
                }
            },
            OutputConfig={
                "S3Bucket": output_bucket,
                "S3Prefix": output_key.rsplit("/", 1)[0] if "/" in output_key else "",
            },
        )

        job_id = response["JobId"]

        # Wait for job completion
        while True:
            status = textract_client.get_document_text_detection(JobId=job_id)
            if status["JobStatus"] in ["SUCCEEDED", "FAILED"]:
                break

        if status["JobStatus"] == "FAILED":
            raise Exception(f"Textract job failed: {status.get('StatusMessage')}")

        # Retrieve and return results
        result = {
            "text": [],
            "blocks": status.get("Blocks", []),
            "provider": "aws_textract",
            "job_id": job_id,
        }

        for block in status.get("Blocks", []):
            if block["BlockType"] == "LINE":
                result["text"].append(block["Text"])

        # Store results in S3
        s3_client.put_object(
            Bucket=output_bucket,
            Key=output_key,
            Body=io.BytesIO(str(result).encode()),
            ContentType="application/json",
        )

        return result
    except ClientError as e:
        raise Exception(f"Failed to run OCR on document: {e}")
