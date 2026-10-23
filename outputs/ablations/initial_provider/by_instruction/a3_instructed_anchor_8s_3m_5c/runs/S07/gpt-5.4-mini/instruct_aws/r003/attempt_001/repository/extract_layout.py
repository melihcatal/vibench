from document_client import load_document_input, s3_object_reference, textract_client
from document_models import LayoutExtractionResult


def extract_layout(bucket: str | None = None, key: str | None = None, version: str | None = None) -> LayoutExtractionResult:
    bucket, key, version = load_document_input(bucket, key, version)
    response = textract_client().analyze_document(Document=s3_object_reference(bucket, key, version), FeatureTypes=["LAYOUT"])
    blocks = response.get("Blocks", [])
    return LayoutExtractionResult(
        blocks=[b for b in blocks if b.get("BlockType") in {"LAYOUT_TEXT", "LAYOUT_TITLE", "LAYOUT_LIST", "LAYOUT_FIGURE", "LAYOUT_TABLE", "LAYOUT_KEY_VALUE"}],
        lines=[b for b in blocks if b.get("BlockType") == "LINE"],
        tables=[b for b in blocks if b.get("BlockType") == "TABLE"],
        raw=response,
    )
