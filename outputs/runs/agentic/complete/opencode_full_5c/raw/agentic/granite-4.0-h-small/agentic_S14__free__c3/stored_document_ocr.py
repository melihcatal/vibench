# [LATER-STEP] stored_document_ocr.py

import boto3
import base64
import json
import tempfile
from io import BytesIO

from storage_client import get_managed_storage_client
from storage_models import ObjectMetadata


def ocr_document(bucket_name: str, object_key: str) -> dict:
    """Run OCR on a stored document (e.g., PDF, image) using AWS Textract.

    Assumes the storage client is S3‑compatible and the bucket contains the file.
    Returns OCR results as a structured dict.
    """
    client = get_managed_storage_client()
    # Download the object bytes.
    response = client.get_object(Bucket=bucket_name, Key=object_key)
    document_bytes = response["Body"].read()

    # Upload bytes temporarily to Textract (needs an S3 bucket). For demo, use same bucket.
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(document_bytes)
        tmp_local_path = tmp_file.name
        tmp_key = f"textract/tmp_{object_key.split('/')[-1]}"

    textract = boto3.client("textract")
    response = textract.start_document_text_detection(
        DocumentLocation={"S3Object": {"Bucket": bucket_name, "Name": tmp_key}}
    )
    job_id = response["JobId"]

    # Poll for completion.
    while True:
        status = textract.get_document_text_detection(JobId=job_id)
        if status["JobStatus"] == "SUCCEEDED":
            result = status["Blocks"]
            break
        elif status["JobStatus"] == "FAILED":
            raise RuntimeError(f"OCR job failed: {status}")
        else:
            continue

    # Clean up temporary file.
    os.unlink(tmp_local_path)
    return result
