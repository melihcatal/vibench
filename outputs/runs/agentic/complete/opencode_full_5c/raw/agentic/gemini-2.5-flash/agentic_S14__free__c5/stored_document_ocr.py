import os
from google.cloud import (
    vision_v1p4beta1 as vision,
)  # Using a newer version for better OCR features if available
from google.protobuf import (
    json_format,
)  # For parsing JSON response if needed, although client returns objects
from storage_client import get_s3_client  # To retrieve the document from S3
from storage_models import OcrRequest, OcrResponse


def run_ocr_on_stored_document(request: OcrRequest) -> OcrResponse:
    # Initialize Google Cloud Vision client
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should point to your service account key file
    vision_client = vision.ImageAnnotatorClient()

    # Retrieve document from S3
    s3_client = get_s3_client()
    try:
        s3_object = s3_client.get_object(
            Bucket=request.bucket_name, Key=request.object_key
        )
        content = s3_object["Body"].read()
    except Exception as e:
        return OcrResponse(
            success=False,
            extracted_text=None,
            message=f"Failed to retrieve document from S3 ({request.bucket_name}/{request.object_key}): {str(e)}",
        )

    # Prepare image for Vision API
    image = vision.Image(content=content)

    # Perform document text detection
    try:
        response = vision_client.document_text_detection(image=image)
        full_text = (
            response.full_text_annotation.text if response.full_text_annotation else ""
        )
        return OcrResponse(
            success=True,
            extracted_text=full_text,
            message=f"OCR performed successfully on {request.object_key}.",
        )
    except Exception as e:
        return OcrResponse(
            success=False,
            extracted_text=None,
            message=f"Failed to perform OCR on {request.object_key}: {str(e)}",
        )
