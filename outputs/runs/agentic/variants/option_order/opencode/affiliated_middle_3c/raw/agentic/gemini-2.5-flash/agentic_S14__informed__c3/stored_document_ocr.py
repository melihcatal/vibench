import time
import json
from storage_client import get_textract_client, get_s3_client
from storage_models import OCRDocumentRequest, OCRDocumentResponse


def run_ocr_on_stored_document(request: OCRDocumentRequest) -> OCRDocumentResponse:
    textract_client = get_textract_client()
    s3_client = get_s3_client()

    try:
        # Start asynchronous document analysis
        start_response = textract_client.start_document_analysis(
            DocumentLocation={
                "S3Object": {"Bucket": request.bucket_name, "Name": request.object_name}
            },
            FeatureTypes=[
                "FORMS",
                "TABLES",
            ],  # You can specify other feature types as needed
        )
        job_id = start_response["JobId"]

        # Poll for job completion (simplified for example, real-world might use SNS/SQS)
        status = "IN_PROGRESS"
        while status == "IN_PROGRESS":
            time.sleep(5)  # Wait for 5 seconds before checking again
            get_response = textract_client.get_document_analysis(JobId=job_id)
            status = get_response["JobStatus"]

        if status == "SUCCEEDED":
            text_content = []
            # Iterate through all pages of results
            next_token = None
            while True:
                if next_token:
                    page_response = textract_client.get_document_analysis(
                        JobId=job_id, NextToken=next_token
                    )
                else:
                    page_response = get_response

                for item in page_response["Blocks"]:
                    if item["BlockType"] == "LINE":
                        text_content.append(item["Text"])

                next_token = page_response.get("NextToken")
                if not next_token:
                    break

            return OCRDocumentResponse(
                success=True,
                message=f"OCR completed successfully for {request.object_name}.",
                text_content="\n".join(text_content),
                raw_response=get_response,
            )
        else:
            return OCRDocumentResponse(
                success=False,
                message=f"OCR job failed for {request.object_name} with status: {status}.",
                raw_response=get_response,
            )

    except Exception as e:
        return OCRDocumentResponse(
            success=False, message=f"Error running OCR: {str(e)}"
        )
