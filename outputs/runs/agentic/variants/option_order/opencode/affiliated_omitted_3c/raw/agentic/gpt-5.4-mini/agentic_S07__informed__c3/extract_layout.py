from typing import Any, Optional

from document_client import build_textract_client, load_bytes, normalize_layout_blocks
from document_models import DocumentRequest, LayoutExtractionResult


def extract_layout(source: Any, *, region_name: Optional[str] = None) -> LayoutExtractionResult:
    request = DocumentRequest.from_input(source)
    client = build_textract_client(region_name=region_name)
    response = client.analyze_document(Document={"Bytes": load_bytes(request)}, FeatureTypes=["LAYOUT"])
    blocks = normalize_layout_blocks(response)
    return LayoutExtractionResult(blocks=blocks, raw=response)
