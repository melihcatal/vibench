from typing import Any, Dict

from document_client import build_textract_client, coerce_document_bytes, infer_document_source
from document_models import normalize_key_value_result


def extract_key_values(document: Any, *, region_name: str = None) -> Dict[str, Any]:
    client = build_textract_client(region_name=region_name)
    payload = coerce_document_bytes(document)
    response = client.analyze_document(
        Document={"Bytes": payload},
        FeatureTypes=["FORMS"],
    )
    return normalize_key_value_result(response, source=infer_document_source(document, "amazon-textract"))
