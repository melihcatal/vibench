from typing import Any

from document_client import get_textract_client
from document_models import LayoutResponse, normalize_blocks


def extract_layout(*, bucket: str = None, key: str = None, bytes_data: bytes = None) -> LayoutResponse:
    client = get_textract_client()
    if bytes_data is not None:
        response = client.analyze_document(Document={"Bytes": bytes_data}, FeatureTypes=["LAYOUT", "TABLES", "FORMS"])
    else:
        if not bucket or not key:
            raise ValueError("bucket and key are required when bytes_data is not provided")
        response = client.analyze_document(Document={"S3Object": {"Bucket": bucket, "Name": key}}, FeatureTypes=["LAYOUT", "TABLES", "FORMS"])
    return LayoutResponse(raw=response, blocks=normalize_blocks(response))
