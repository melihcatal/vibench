from document_client import get_document_analysis_client, load_image_bytes
from document_models import LayoutResult, normalize_layout_response


AZURE_LAYOUT_MODEL_ID = "prebuilt-layout"


def extract_layout_from_image(image_path: str) -> LayoutResult:
    client = get_document_analysis_client()
    image_bytes = load_image_bytes(image_path)
    poller = client.begin_analyze_document(
        model_id=AZURE_LAYOUT_MODEL_ID, document=image_bytes
    )
    result = poller.result()
    return normalize_layout_response(result)


def extract_layout_from_bytes(image_bytes: bytes) -> LayoutResult:
    client = get_document_analysis_client()
    poller = client.begin_analyze_document(
        model_id=AZURE_LAYOUT_MODEL_ID, document=image_bytes
    )
    result = poller.result()
    return normalize_layout_response(result)


def get_text_blocks(layout_result: LayoutResult):
    return [
        block
        for block in layout_result.blocks
        if block.kind in ("paragraph", "sectionHeading", "title")
    ]


def get_tables_from_layout(layout_result: LayoutResult):
    return layout_result.tables


def get_layout_summary(layout_result: LayoutResult) -> dict:
    return {
        "page_count": len(layout_result.pages),
        "block_count": len(layout_result.blocks),
        "table_count": len(layout_result.tables),
        "model_id": layout_result.model_id,
    }
