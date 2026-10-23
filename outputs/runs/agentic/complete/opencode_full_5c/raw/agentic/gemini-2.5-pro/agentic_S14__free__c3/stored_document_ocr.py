import time
from storage_client import get_textract_client
from storage_models import OcrRequest


def run_document_ocr(request: OcrRequest) -> str:
    """
    Starts an OCR job for a document in S3 using Amazon Textract
    and polls for its completion.
    """
    textract_client = get_textract_client()

    response = textract_client.start_document_text_detection(
        DocumentLocation={
            "S3Object": {
                "Bucket": request.s3_object.bucket,
                "Name": request.s3_object.key,
            }
        }
    )

    job_id = response["JobId"]
    status = "IN_PROGRESS"

    while status == "IN_PROGRESS":
        time.sleep(5)
        job_result = textract_client.get_document_text_detection(JobId=job_id)
        status = job_result["JobStatus"]

    if status == "SUCCEEDED":
        text = ""
        for item in job_result.get("Blocks", []):
            if item["BlockType"] == "LINE":
                text += item["Text"] + "\n"
        return text
    else:
        return f"OCR job failed with status: {status}"
