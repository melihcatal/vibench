import logging
import time
from storage_client import get_textract_client, get_s3_client
from storage_models import OcrResult

logger = logging.getLogger(__name__)


def run_ocr_on_document(bucket_name: str, object_key: str) -> OcrResult:
    textract_client = get_textract_client()
    s3_client = get_s3_client()

    # Check if the object exists first
    try:
        s3_client.head_object(Bucket=bucket_name, Key=object_key)
    except s3_client.exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "404":
            logger.error(f"Document {object_key} not found in bucket {bucket_name}.")
            raise FileNotFoundError(f"Document {object_key} not found.")
        else:
            logger.error(
                f"Error accessing document {object_key} in bucket {bucket_name}: {e}"
            )
            raise

    try:
        response = textract_client.start_document_analysis(
            DocumentLocation={"S3Object": {"Bucket": bucket_name, "Name": object_key}},
            FeatureTypes=[
                "FORMS",
                "TABLES",
            ],  # Or just ['TEXT'] if only text extraction is needed
        )
        job_id = response["JobId"]
        logger.info(f"Started Textract job with ID: {job_id}")

        # Poll for job completion (simplified for example, in real-world use a notification system)
        max_attempts = 60
        attempts = 0
        while attempts < max_attempts:
            job_status_response = textract_client.get_document_analysis(JobId=job_id)
            job_status = job_status_response["JobStatus"]
            logger.debug(f"Textract job {job_id} status: {job_status}")

            if job_status in ["SUCCEEDED", "FAILED", "PARTIAL_SUCCESS", "STOPPED"]:
                break

            time.sleep(5)  # Wait 5 seconds before checking again
            attempts += 1

        if job_status == "SUCCEEDED":
            extracted_text = []
            # Get results, handling pagination
            next_token = None
            while True:
                if next_token:
                    page_response = textract_client.get_document_analysis(
                        JobId=job_id, NextToken=next_token
                    )
                else:
                    page_response = job_status_response  # Use the initial response for the first page

                for block in page_response["Blocks"]:
                    if block["BlockType"] == "LINE":
                        extracted_text.append(block["Text"])
                next_token = page_response.get("NextToken")
                if not next_token:
                    break

            return OcrResult(extracted_text="\n".join(extracted_text))
        else:
            logger.error(
                f"Textract job {job_id} failed with status: {job_status}. Details: {job_status_response.get('StatusMessage')}"
            )
            raise Exception(f"Textract job failed: {job_status}")

    except Exception as e:
        logger.error(
            f"Error running OCR on document {object_key} in bucket {bucket_name}: {e}"
        )
        raise
