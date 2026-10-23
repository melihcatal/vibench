import time
from storage_client import get_textract_client


def run_ocr_on_document(bucket_name: str, document_name: str) -> dict:
    """
    Performs OCR on a document stored in S3 using Amazon Textract.
    This function uses synchronous detection.
    """
    textract_client = get_textract_client()

    try:
        response = textract_client.detect_document_text(
            Document={"S3Object": {"Bucket": bucket_name, "Name": document_name}}
        )

        extracted_text = []
        for item in response["Blocks"]:
            if item["BlockType"] == "LINE":
                extracted_text.append(item["Text"])

        return {"status": "succeeded", "text": "\n".join(extracted_text)}

    except Exception as e:
        return {"status": "failed", "error": str(e)}
