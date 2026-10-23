from typing import Any, Optional

from document_client import build_textract_client, load_bytes, normalize_tables
from document_models import DocumentRequest, TableExtractionResult


def extract_tables(source: Any, *, region_name: Optional[str] = None) -> TableExtractionResult:
    request = DocumentRequest.from_input(source)
    client = build_textract_client(region_name=region_name)
    response = client.analyze_document(Document={"Bytes": load_bytes(request)}, FeatureTypes=["TABLES"])
    tables = normalize_tables(response)
    return TableExtractionResult(tables=tables, raw=response)
