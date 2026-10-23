import os
from typing import Optional
from document_client import DocumentClient
from document_models import DocumentTextResult


def extract_text_from_image(
    image_path: str, region: Optional[str] = None
) -> DocumentTextResult:
    client = DocumentClient(region_name=region)
    textract_client = client.get_textract_client()

    image_bytes = client.read_image_bytes(image_path)
    request = client.prepare_textract_request(image_bytes)

    response = textract_client.detect_document_text(**request)

    return DocumentTextResult.from_textract_response(response)


def extract_text_from_bytes(
    image_bytes: bytes, region: Optional[str] = None
) -> DocumentTextResult:
    client = DocumentClient(region_name=region)
    textract_client = client.get_textract_client()

    request = {"Document": {"Bytes": image_bytes}}
    response = textract_client.detect_document_text(**request)

    return DocumentTextResult.from_textract_response(response)


def extract_text_with_analysis(
    image_path: str, region: Optional[str] = None
) -> DocumentTextResult:
    client = DocumentClient(region_name=region)
    textract_client = client.get_textract_client()

    image_bytes = client.read_image_bytes(image_path)
    request = client.prepare_textract_request(image_bytes)

    features = client.get_textract_features("text")
    request["FeatureTypes"] = features

    response = textract_client.analyze_document(**request)

    return DocumentTextResult.from_textract_response(response)
