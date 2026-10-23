from typing import Optional

from document_client import (
    get_textract_client,
    build_textract_image_bytes,
    normalize_textract_response,
)
from document_models import LayoutResponse, normalize_layout_response


TEXTRACT_MODEL_ID = "aws:textract:analyze"


def extract_layout_from_image(
    image_path: Optional[str] = None,
    image_bytes: Optional[bytes] = None,
) -> LayoutResponse:
    client = get_textract_client()
    image_doc = build_textract_image_bytes(
        image_path=image_path, image_bytes=image_bytes
    )
    response = client.analyze_document(
        Document=image_doc,
        FeatureTypes=["LAYOUT"],
    )
    normalized = normalize_textract_response(response)
    result = normalize_layout_response(normalized)
    return result


def extract_layout_with_tables(
    image_path: Optional[str] = None,
    image_bytes: Optional[bytes] = None,
) -> LayoutResponse:
    client = get_textract_client()
    image_doc = build_textract_image_bytes(
        image_path=image_path, image_bytes=image_bytes
    )
    response = client.analyze_document(
        Document=image_doc,
        FeatureTypes=["LAYOUT", "TABLES"],
    )
    normalized = normalize_textract_response(response)
    result = normalize_layout_response(normalized)
    return result


def extract_layout_with_forms(
    image_path: Optional[str] = None,
    image_bytes: Optional[bytes] = None,
) -> LayoutResponse:
    client = get_textract_client()
    image_doc = build_textract_image_bytes(
        image_path=image_path, image_bytes=image_bytes
    )
    response = client.analyze_document(
        Document=image_doc,
        FeatureTypes=["LAYOUT", "FORMS"],
    )
    normalized = normalize_textract_response(response)
    result = normalize_layout_response(normalized)
    return result


def extract_full_layout(
    image_path: Optional[str] = None,
    image_bytes: Optional[bytes] = None,
) -> LayoutResponse:
    client = get_textract_client()
    image_doc = build_textract_image_bytes(
        image_path=image_path, image_bytes=image_bytes
    )
    response = client.analyze_document(
        Document=image_doc,
        FeatureTypes=["LAYOUT", "TABLES", "FORMS"],
    )
    normalized = normalize_textract_response(response)
    result = normalize_layout_response(normalized)
    return result
