import json
from storage_client import get_textract_client
from storage_models import OcrRequest


def run_document_ocr(request: OcrRequest) -> str:
    """
    Starts an asynchronous OCR job for a document in S3 using Amazon Textract.
    """
    textract_client = get_textract_client()

    response = textract_client.start_document_text_detection(
        DocumentLocation={
            "S3Object": {
                "Bucket": request.storage_object.bucket,
                "Name": request.storage_object.key,
            }
        }
    )

    job_id = response["JobId"]

    # In a real application, you would store this job_id and have a separate
    # process to check for completion and retrieve the results.
    # For this example, we'll just return the job id.

    # Wait for the job to complete
    waiter = textract_client.get_waiter("document_text_detection_completed")
    waiter.wait(JobId=job_id)

    # Get the results
    result_pages = []
    paginator = textract_client.get_paginator("get_document_text_detection")
    pages = paginator.paginate(JobId=job_id)

    text_content = ""
    for page in pages:
        for item in page["Blocks"]:
            if item["BlockType"] == "LINE":
                text_content += item["Text"] + "\n"

    return text_content
