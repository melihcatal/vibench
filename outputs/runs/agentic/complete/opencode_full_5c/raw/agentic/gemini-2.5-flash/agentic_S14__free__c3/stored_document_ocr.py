import time
from storage_client import get_textract_client
from storage_models import StoredDocumentOCRRequest, StoredDocumentOCRResponse
from botocore.exceptions import ClientError


def run_ocr_on_stored_document(
    request: StoredDocumentOCRRequest,
) -> StoredDocumentOCRResponse:
    textract_client = get_textract_client()
    try:
        # Start asynchronous OCR job using AWS Textract
        # This is suitable for larger documents or when immediate results are not required.
        start_response = textract_client.start_document_text_detection(
            DocumentLocation={
                "S3Object": {"Bucket": request.bucket_name, "Name": request.object_key}
            }
        )
        job_id = start_response["JobId"]

        # Poll for job completion
        status = "IN_PROGRESS"
        extracted_text = []
        raw_response = {}

        while status == "IN_PROGRESS":
            time.sleep(5)  # Wait for 5 seconds before polling again
            get_response = textract_client.get_document_text_detection(JobId=job_id)
            status = get_response["JobStatus"]

            if status == "SUCCEEDED":
                # Collect all text blocks
                for item in get_response["Blocks"]:
                    if item["BlockType"] == "WORD" or item["BlockType"] == "LINE":
                        if "Text" in item:
                            extracted_text.append(item["Text"])
                raw_response = get_response
                break
            elif status == "FAILED":
                return StoredDocumentOCRResponse(
                    success=False,
                    message="AWS Textract job failed.",
                    raw_response=get_response,
                )

        return StoredDocumentOCRResponse(
            success=True,
            message="OCR completed successfully",
            extracted_text=" ".join(extracted_text),
            raw_response=raw_response,
        )
    except ClientError as e:
        return StoredDocumentOCRResponse(
            success=False, message=f"AWS Textract ClientError: {e}"
        )
    except Exception as e:
        return StoredDocumentOCRResponse(
            success=False, message=f"An unexpected error occurred: {e}"
        )
