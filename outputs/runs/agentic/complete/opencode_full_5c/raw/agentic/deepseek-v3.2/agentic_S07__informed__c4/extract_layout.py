import os
from typing import List, Dict, Any, Optional
from document_client import DocumentClient
from document_models import (
    LayoutExtractionRequest,
    LayoutBlock,
    LayoutExtractionResponse,
)


def extract_layout(
    image_path: str, mime_type: Optional[str] = None
) -> LayoutExtractionResponse:
    """
    Extract blocks, lines, tables, or layout elements from a document using Azure Document Intelligence.
    """
    client = DocumentClient.get_azure_document_client()

    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")

    with open(image_path, "rb") as f:
        image_content = f.read()

    poller = client.begin_analyze_document(
        model_id="prebuilt-layout",
        document=image_content,
        content_type=mime_type or "image/jpeg",
    )

    result = poller.result()

    blocks = []
    for page in result.pages:
        for line in page.lines:
            block = LayoutBlock(
                text=line.content,
                bounding_box=[(point.x, point.y) for point in line.polygon],
                confidence=line.confidence,
                block_type="line",
            )
            blocks.append(block)

        for table in page.tables:
            for cell in table.cells:
                block = LayoutBlock(
                    text=cell.content,
                    bounding_box=[(point.x, point.y) for point in cell.polygon],
                    confidence=cell.confidence,
                    block_type="table_cell",
                    row_index=cell.row_index,
                    column_index=cell.column_index,
                )
                blocks.append(block)

    return LayoutExtractionResponse(
        blocks=blocks,
        raw_response=result.to_dict(),
        provider="azure_document_intelligence",
    )
