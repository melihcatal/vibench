from typing import Any, Optional

from document_client import build_textract_client, load_bytes, normalize_key_values
from document_models import DocumentRequest, KeyValueExtractionResult


def extract_key_values(source: Any, *, region_name: Optional[str] = None) -> KeyValueExtractionResult:
    request = DocumentRequest.from_input(source)
    client = build_textract_client(region_name=region_name)
    response = client.analyze_document(Document={"Bytes": load_bytes(request)}, FeatureTypes=["FORMS"])
    key_values = normalize_key_values(response)
    return KeyValueExtractionResult(key_values=key_values, raw=response)
