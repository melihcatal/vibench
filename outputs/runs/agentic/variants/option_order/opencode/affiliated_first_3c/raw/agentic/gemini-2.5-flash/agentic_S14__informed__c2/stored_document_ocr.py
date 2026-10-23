from storage_client import get_textract_client
from typing import Dict, Any


def run_ocr_on_stored_document(bucket_name: str, object_key: str) -> Dict[str, Any]:
    """
    Runs OCR on a stored document object in Amazon S3 using Amazon Textract.
    Returns the detected text and other document analysis results.
    """
    textract_client = get_textract_client()
    response = textract_client.analyze_document(
        Document={"S3Object": {"Bucket": bucket_name, "Name": object_key}},
        FeatureTypes=[
            "FORMS",
            "TABLES",
        ],  # You can customize feature types based on needs
    )
    return response
