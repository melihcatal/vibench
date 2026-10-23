import time
from typing import List
from storage_client import get_textract_client
from storage_models import StorageObject, OCRResult


def run_ocr_on_document(
    storage_object: StorageObject,
) -> List[OCRResult]:
    textract_client = get_textract_client()
    results = []

    try:
        response = textract_client.start_document_text_detection(
            DocumentLocation={
                "S3Object": {
                    "Bucket": storage_object.bucket,
                    "Name": storage_object.key,
                }
            }
        )
        job_id = response["JobId"]

        while True:
            job_status = textract_client.get_document_text_detection(JobId=job_id)
            status = job_status["JobStatus"]
            if status in ["SUCCEEDED", "FAILED"]:
                break
            time.sleep(5)

        if status == "SUCCEEDED":
            blocks = []
            next_token = None
            while True:
                kwargs = {"JobId": job_id}
                if next_token:
                    kwargs["NextToken"] = next_token
                page_result = textract_client.get_document_text_detection(**kwargs)
                blocks.extend(page_result["Blocks"])
                next_token = page_result.get("NextToken")
                if not next_token:
                    break

            for block in blocks:
                if block["BlockType"] == "LINE":
                    results.append(
                        OCRResult(
                            text=block["Text"], confidence=block["Confidence"] / 100.0
                        )
                    )

    except Exception as e:
        print(f"Error running OCR: {e}")

    return results
