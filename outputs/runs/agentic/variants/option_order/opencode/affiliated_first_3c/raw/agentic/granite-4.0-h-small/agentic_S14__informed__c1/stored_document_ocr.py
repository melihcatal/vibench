# stored_document_ocr.py
# [LATER-STEP] Run OCR on a stored document object using Amazon Textract (SDK example)

import os
import boto3
from storage_client import create_s3_client
from storage_models import OCRResult


def ocr_document(bucket: str, key: str) -> OCRResult:
    """Runs text detection (OCR) on a stored document (e.g., PDF, image) using Amazon Textract.
    Args:
        bucket (str): Bucket containing the document.
        key (str): Object key of the document.
    Returns:
        OCRResult: Extracted plain text and optional character bounding boxes.
    """
    textract = boto3.client("textract")  # Uses same credentials as create_s3_client
    response = textract.detect_document_text(
        Document={"S3Object": {"Bucket": bucket, "Key": key}}
    )
    # Extract plain text and (optionally) geometry data
    text_lines = [
        block["Text"] for block in response["Blocks"] if block["BlockType"] == "LINE"
    ]
    text = "\n".join(text_lines)
    # Geometry (bounding box) info can be collected here if needed
    boxes = []  # TODO: Populate if required
    return OCRResult(text=text, boxes=boxes)


# Example usage (uncomment to test)
# result = ocr_document('my-bucket', 'sample.pdf')
# print('Extracted text:', result.text[:200])
