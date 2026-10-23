from typing import Optional

from document_client import (
    get_textract_client,
    build_textract_image_bytes,
    normalize_textract_response,
)
from document_models import KeyValueResponse, normalize_kv_response


TEXTRACT_MODEL_ID = "aws:textract:forms"


def extract_key_values_from_image(
    image_path: Optional[str] = None,
    image_bytes: Optional[bytes] = None,
) -> KeyValueResponse:
    client = get_textract_client()
    image_doc = build_textract_image_bytes(
        image_path=image_path, image_bytes=image_bytes
    )
    response = client.analyze_document(
        Document=image_doc,
        FeatureTypes=["FORMS"],
    )
    normalized = normalize_textract_response(response)
    result = normalize_kv_response(normalized)
    return result


def extract_key_values_with_tables(
    image_path: Optional[str] = None,
    image_bytes: Optional[bytes] = None,
) -> KeyValueResponse:
    client = get_textract_client()
    image_doc = build_textract_image_bytes(
        image_path=image_path, image_bytes=image_bytes
    )
    response = client.analyze_document(
        Document=image_doc,
        FeatureTypes=["FORMS", "TABLES"],
    )
    normalized = normalize_textract_response(response)
    result = normalize_kv_response(normalized)
    return result


def extract_key_values_from_s3(
    bucket: str,
    key: str,
    version: Optional[str] = None,
) -> KeyValueResponse:
    client = get_textract_client()
    s3_object = {"Bucket": bucket, "Name": key}
    if version:
        s3_object["Version"] = version
    response = client.analyze_document(
        Document={"S3Object": s3_object},
        FeatureTypes=["FORMS"],
    )
    normalized = normalize_textract_response(response)
    result = normalize_kv_response(normalized)
    return result


def get_key_value_dict(kv_response: KeyValueResponse) -> dict:
    result = {}
    for kv in kv_response.key_values:
        result[kv.key] = kv.value
    return result
