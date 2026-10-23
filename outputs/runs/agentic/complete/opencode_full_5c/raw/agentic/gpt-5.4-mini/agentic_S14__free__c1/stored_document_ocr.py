import base64

from storage_client import get_textract_client, resolve_bucket


def stored_document_ocr(bucket: str, key: str):
    textract = get_textract_client()
    response = textract.start_document_text_detection(
        DocumentLocation={"S3Object": {"Bucket": resolve_bucket(bucket), "Name": key}}
    )
    return {"job_id": response.get("JobId"), "status": response.get("JobStatus")}
