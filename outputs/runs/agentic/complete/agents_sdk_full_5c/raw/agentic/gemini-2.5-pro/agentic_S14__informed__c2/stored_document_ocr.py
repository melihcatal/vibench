import boto3
import time
from typing import List


def run_ocr_on_s3_document(bucket_name: str, document_key: str) -> str:
    """
    Performs OCR on a document stored in S3 using Amazon Textract.
    This function starts a job and waits for its completion.

    :param bucket_name: The S3 bucket where the document is stored.
    :param document_key: The key (path) of the document in the S3 bucket.
    :return: Extracted text as a single string.
    """
    textract_client = boto3.client("textract")

    response = textract_client.start_document_text_detection(
        DocumentLocation={"S3Object": {"Bucket": bucket_name, "Name": document_key}}
    )
    job_id = response["JobId"]
    print(f"Started Textract job with ID: {job_id}")

    job_status = "IN_PROGRESS"
    while job_status == "IN_PROGRESS":
        time.sleep(5)
        job_result = textract_client.get_document_text_detection(JobId=job_id)
        job_status = job_result["JobStatus"]
        print(f"Job status: {job_status}")

    if job_status == "SUCCEEDED":
        blocks = []
        paginator = textract_client.get_paginator("get_document_text_detection")
        pages = paginator.paginate(JobId=job_id)
        for page in pages:
            blocks.extend(page["Blocks"])
        
        lines = [
            block["Text"] for block in blocks if block["BlockType"] == "LINE"
        ]
        return "\n".join(lines)
    else:
        return f"OCR job failed with status: {job_status}"
