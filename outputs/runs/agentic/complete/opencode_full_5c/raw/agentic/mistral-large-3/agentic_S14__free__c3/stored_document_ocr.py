from typing import BinaryIO, Optional

import boto3
from botocore.exceptions import ClientError
from google.cloud import vision_v1
from google.cloud.vision_v1 import types

from storage_client import get_storage_client
from storage_models import ObjectMetadataResponse


def run_ocr_on_stored_document(
    bucket_name: str,
    object_key: str,
    language_hints: Optional[list] = None,
) -> str:
    """
    Runs OCR on a document stored in AWS S3 using Google Cloud Vision API.

    Args:
        bucket_name: Name of the S3 bucket.
        object_key: Key/path of the object in the bucket.
        language_hints: Optional list of language hints for OCR.

    Returns:
        Extracted text from the document.

    Raises:
        ClientError: If the OCR process fails.
    """
    s3_client = get_storage_client()
    vision_client = vision_v1.ImageAnnotatorClient()

    try:
        # Fetch the object from S3
        response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
        content = response["Body"].read()

        # Perform OCR using Google Cloud Vision
        image = types.Image(content=content)
        features = [types.Feature(type_=types.Feature.Type.DOCUMENT_TEXT_DETECTION)]

        request = types.AnnotateImageRequest(
            image=image,
            features=features,
            image_context=types.ImageContext(language_hints=language_hints)
            if language_hints
            else None,
        )

        response = vision_client.batch_annotate_images(requests=[request])
        annotations = response.responses[0]

        if annotations.error.message:
            raise ClientError(
                error_response={
                    "Error": {"Code": "OCR_ERROR", "Message": annotations.error.message}
                },
                operation_name="run_ocr_on_stored_document",
            )

        return annotations.full_text_annotation.text
    except Exception as e:
        raise ClientError(
            error_response={"Error": {"Code": "OCR_FAILED", "Message": str(e)}},
            operation_name="run_ocr_on_stored_document",
        )
