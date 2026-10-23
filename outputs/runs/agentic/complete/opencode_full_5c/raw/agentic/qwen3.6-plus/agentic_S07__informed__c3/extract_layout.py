from document_client import get_azure_document_client, load_image_bytes
from document_models import LayoutBlock, LayoutResult


def extract_layout_from_image(image_path: str) -> list[LayoutResult]:
    client = get_azure_document_client()
    image_bytes = load_image_bytes(image_path)
    poller = client.begin_analyze_document(model_id="prebuilt-layout", body=image_bytes)
    result = poller.result()
    layout_results = []
    for page in result.pages:
        blocks = []
        if page.selection_marks:
            for mark in page.selection_marks:
                blocks.append(
                    LayoutBlock(
                        content="selected"
                        if mark.state == "selected"
                        else "unselected",
                        bounding_box=mark.polygon,
                        category="selectionMark",
                        confidence=mark.confidence,
                    )
                )
        for line in page.lines or []:
            blocks.append(
                LayoutBlock(
                    content=line.content,
                    bounding_box=line.polygon,
                    category="line",
                    confidence=1.0,
                )
            )
        layout_results.append(
            LayoutResult(blocks=blocks, page_width=page.width, page_height=page.height)
        )
    return layout_results
