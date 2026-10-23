from typing import Any, Dict, Union

from document_client import textract_client
from document_models import normalize_blocks


def extract_layout(document: Union[str, bytes, Dict[str, Any]]) -> Dict[str, Any]:
    client = textract_client()
    if isinstance(document, bytes):
        response = client.analyze_document(Document={"Bytes": document}, FeatureTypes=["LAYOUT"])
    else:
        response = client.analyze_document(Document=document, FeatureTypes=["LAYOUT"])
    return {"blocks": normalize_blocks(response.get("Blocks", [])), "raw": response}
