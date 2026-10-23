# [LATER-STEP] stored_document_ocr.py

# Uses Alibaba Cloud Document AI OCR for processing stored documents.
# Provider: Alibaba Cloud Document AI OCR
# SDK: dashscope
# Auth: DASHSCOPE_API_KEY

import os
import json
from dashscope.vision import ocr
from .storage_client import get_s3_client
from .storage_client import get_bucket_name


# Helper to download object content into memory
def _download_object(bucket: str, key: str) -> bytes:
    s3 = get_s3_client()
    response = s3.get_object(Bucket=bucket, Key=key)
    return response["Body"].read()


# Public entry point
async def run_ocr_on_document(object_key: str, bucket_name: str = None) -> dict:
    """Runs OCR on a stored PDF/Docx/Img document and returns extracted text and layout.

    Args:
        object_key: S3 key of the document.
        bucket_name: Optional bucket; falls back to env var.

    Returns:
        dict containing `text`, `blocks`, `layout`, `pageCount`, etc.
    """
    if bucket_name is None:
        bucket_name = get_bucket_name()

    content = _download_object(bucket_name, object_key)
    # Alibaba Cloud's OCR accepts image bytes directly; for PDFs we first convert to images
    # Here we offload conversion to the provider's API for simplicity.
    result = ocr(image_bytes=content)
    # Alibaba returns a JSON structure
    return {
        "text": result.get("text"),
        "blocks": result.get("blocks"),
        "layout": result.get("layout"),
        "pageCount": result.get("pageCount"),
    }


# Example usage (uncomment to test)
# if __name__ == '__main__':
#     print(run_ocr_on_document('sample.pdf'))
