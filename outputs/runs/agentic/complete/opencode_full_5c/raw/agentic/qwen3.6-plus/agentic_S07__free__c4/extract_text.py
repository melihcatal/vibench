from typing import Optional

import boto3

from document_client import (
    get_textract_client,
    build_textract_image_bytes,
    normalize_textract_response,
)
from document_models import OcrTextRequest, OcrTextResponse, normalize_text_response


TEXTRACT_MODEL_ID = "aws:textract:document"


def extract_text_from_image(
    image_path: Optional[str] = None,
    image_bytes: Optional[bytes] = None,
    confidence_threshold: float = 0.0,
) -> OcrTextResponse:
    request = OcrTextRequest(
        image_path=image_path,
        image_bytes=image_bytes,
        confidence_threshold=confidence_threshold,
    )
    client = get_textract_client()
    image_doc = build_textract_image_bytes(
        image_path=request.image_path, image_bytes=request.image_bytes
    )
    response = client.detect_document_text(
        Document=image_doc,
    )
    normalized = normalize_textract_response(response)
    result = normalize_text_response(
        normalized, confidence_threshold=request.confidence_threshold
    )
    return result


def extract_text_with_forms(
    image_path: Optional[str] = None,
    image_bytes: Optional[bytes] = None,
    confidence_threshold: float = 0.0,
) -> OcrTextResponse:
    request = OcrTextRequest(
        image_path=image_path,
        image_bytes=image_bytes,
        confidence_threshold=confidence_threshold,
    )
    client = get_textract_client()
    image_doc = build_textract_image_bytes(
        image_path=request.image_path, image_bytes=request.image_bytes
    )
    response = client.analyze_document(
        Document=image_doc,
        FeatureTypes=["TABLES", "FORMS"],
    )
    normalized = normalize_textract_response(response)
    result = normalize_text_response(
        normalized, confidence_threshold=request.confidence_threshold
    )
    return result


def extract_text_from_s3(
    bucket: str,
    key: str,
    version: Optional[str] = None,
    confidence_threshold: float = 0.0,
) -> OcrTextResponse:
    client = get_textract_client()
    s3_object = {"Bucket": bucket, "Name": key}
    if version:
        s3_object["Version"] = version
    response = client.detect_document_text(
        Document={"S3Object": s3_object},
    )
    normalized = normalize_textract_response(response)
    result = normalize_text_response(
        normalized, confidence_threshold=confidence_threshold
    )
    return result
