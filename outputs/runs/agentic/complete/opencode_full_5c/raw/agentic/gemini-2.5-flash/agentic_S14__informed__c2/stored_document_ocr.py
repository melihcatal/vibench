import time
from typing import Dict, Any, List
from storage_client import get_textract_client, get_s3_client
from storage_models import OcrDocumentRequest, OcrDocumentResponse


def run_ocr_on_stored_document(request: OcrDocumentRequest) -> OcrDocumentResponse:
    textract_client = get_textract_client()
    s3_client = get_s3_client()

    try:
        # Start asynchronous document analysis for text detection
        start_response = textract_client.start_document_text_detection(
            DocumentLocation={
                "S3Object": {"Bucket": request.bucket_name, "Name": request.key}
            }
        )
        job_id = start_response["JobId"]

        # Poll for job completion (simplified for example, real-world might use SNS/SQS)
        print(f"Started Textract job with ID: {job_id}. Polling for results...")
        status = "IN_PROGRESS"
        document_text = ""
        pages: List[Dict[str, Any]] = []

        while status == "IN_PROGRESS":
            time.sleep(5)  # Wait for 5 seconds before polling again
            get_response = textract_client.get_document_text_detection(JobId=job_id)
            status = get_response["JobStatus"]
            print(f"Textract job status: {status}")

        if status == "SUCCEEDED":
            # Retrieve all pages of results
            next_token = None
            while True:
                if next_token:
                    get_response = textract_client.get_document_text_detection(
                        JobId=job_id, NextToken=next_token
                    )
                else:
                    get_response = textract_client.get_document_text_detection(
                        JobId=job_id
                    )

                for block in get_response.get("Blocks", []):
                    if block["BlockType"] == "LINE":
                        document_text += block["Text"] + "\n"
                pages.append(
                    get_response
                )  # Store full page response for detailed parsing

                next_token = get_response.get("NextToken")
                if not next_token:
                    break

            return OcrDocumentResponse(
                job_id=job_id,
                document_text=document_text.strip(),
                pages=pages,  # Can be further processed to extract specific layout info
            )
        else:
            raise RuntimeError(f"Textract job {job_id} failed with status: {status}")

    except Exception as e:
        raise RuntimeError(
            f"Failed to run OCR on document {request.key} in {request.bucket_name}: {e}"
        )
