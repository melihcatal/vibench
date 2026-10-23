# Run OCR on a stored document (AWS Textract provider)
import os
from storage_client import create_s3_client
import boto3


def ocr_document(bucket: str, key: str):
    """Perform OCR on the PDF/DOC stored at `bucket`/`key` and return extracted text blocks."""
    client = create_s3_client()
    textract = boto3.client("textract")

    response = textract.start_document_text_detection(
        DocumentLocation={"S3Object": {"Bucket": bucket, "Name": key}}
    )
    job_id = response["JobId"]

    # Poll until job completes (simple busy‑wait; adjust timeout as needed)
    while True:
        status = textract.get_document_text_detection(JobId=job_id)
        if status["JobStatus"] in ("SUCCEEDED", "FAILED"):
            break
        # brief pause before polling again
        import time

        time.sleep(1)

    if status["JobStatus"] != "SUCCEEDED":
        raise RuntimeError(f"OCR job failed: {status}")

    text_blocks = [
        block["Text"]
        for block in status.get("Blocks", [])
        if block["BlockType"] == "LINE"
    ]
    return "\n".join(text_blocks)
