# stored_document_ocr.py
# [LATER-STEP] Run OCR on a stored document object
# Using AWS Rekognition as the concrete managed image/OCR provider
import boto3
from storage_client import get_s3_client
from storage_models import ObjectMetadataResponse, DownloadResponse
from typing import Optional, Any


def ocr_document(object_key: str) -> dict:
    """Extract text from a stored document (e.g., PDF, image) using AWS Rekognition.

    The function first downloads the object to a temporary location, then runs
    Rekognition's DetectDocumentText API, and finally returns the extracted text.
    """
    # Resolve bucket name from env or default
    bucket = get_s3_client().meta.client.get_bucket_location(Bucket="")
    # Determine bucket name (Rekognition needs bucket and key, download URL not needed)
    # Download the object to a temporary file
    import tempfile
    import os

    tmp_file = tempfile.NamedTemporaryFile(delete=False)
    obj = get_s3_client().get_object(
        Bucket=bucket["LocationConstraint"] or "", Key=object_key
    )
    tmp_file.write(obj["Body"].read())
    tmp_file.close()

    rekog = boto3.client("rekognition")
    with open(tmp_file.name, "rb") as img:
        response = rekog.detect_document_text(Image={"Bytes": img.read()})
    os.remove(tmp_file.name)
    return response
