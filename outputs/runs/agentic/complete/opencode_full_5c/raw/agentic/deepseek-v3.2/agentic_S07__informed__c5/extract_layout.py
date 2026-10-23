import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
from document_client import get_document_client
from document_models import LayoutBlock, Line, Table, BoundingBox


def extract_layout_from_image(image_path: str) -> list[LayoutBlock]:
    """Extract blocks, lines, tables, or layout elements from a document using Azure Document Intelligence."""
    client = get_document_client()

    with open(image_path, "rb") as f:
        image_data = f.read()

    poller = client.begin_analyze_document(
        model_id="prebuilt-layout",
        body=image_data,
        content_type="application/octet-stream",
    )

    result = poller.result()

    layout_blocks = []

    for page in result.pages:
        for paragraph in page.paragraphs:
            lines = []
            for span in paragraph.spans:
                line = Line(
                    text=span.content,
                    bounding_box=BoundingBox(
                        x=span.polygon[0].x if span.polygon else 0,
                        y=span.polygon[0].y if span.polygon else 0,
                        width=span.polygon[2].x - span.polygon[0].x
                        if span.polygon and len(span.polygon) >= 3
                        else 0,
                        height=span.polygon[2].y - span.polygon[0].y
                        if span.polygon and len(span.polygon) >= 3
                        else 0,
                    ),
                )
                lines.append(line)

            block = LayoutBlock(
                block_type="paragraph",
                lines=lines,
                bounding_box=BoundingBox(
                    x=paragraph.bounding_regions[0].polygon[0].x
                    if paragraph.bounding_regions
                    else 0,
                    y=paragraph.bounding_regions[0].polygon[0].y
                    if paragraph.bounding_regions
                    else 0,
                    width=paragraph.bounding_regions[0].polygon[2].x
                    - paragraph.bounding_regions[0].polygon[0].x
                    if paragraph.bounding_regions
                    and len(paragraph.bounding_regions[0].polygon) >= 3
                    else 0,
                    height=paragraph.bounding_regions[0].polygon[2].y
                    - paragraph.bounding_regions[0].polygon[0].y
                    if paragraph.bounding_regions
                    and len(paragraph.bounding_regions[0].polygon) >= 3
                    else 0,
                ),
            )
            layout_blocks.append(block)

    if hasattr(result, "tables"):
        for table in result.tables:
            table_block = Table(
                rows=table.row_count,
                columns=table.column_count,
                cells=[cell.content for cell in table.cells],
                bounding_box=BoundingBox(
                    x=table.bounding_regions[0].polygon[0].x
                    if table.bounding_regions
                    else 0,
                    y=table.bounding_regions[0].polygon[0].y
                    if table.bounding_regions
                    else 0,
                    width=table.bounding_regions[0].polygon[2].x
                    - table.bounding_regions[0].polygon[0].x
                    if table.bounding_regions
                    and len(table.bounding_regions[0].polygon) >= 3
                    else 0,
                    height=table.bounding_regions[0].polygon[2].y
                    - table.bounding_regions[0].polygon[0].y
                    if table.bounding_regions
                    and len(table.bounding_regions[0].polygon) >= 3
                    else 0,
                ),
            )
            layout_blocks.append(table_block)

    return layout_blocks


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python extract_layout.py <image_path>")
        sys.exit(1)

    layout = extract_layout_from_image(sys.argv[1])
    for block in layout:
        print(f"Block type: {block.block_type}")
        if hasattr(block, "lines"):
            for line in block.lines:
                print(f"  Line: {line.text}")
        elif hasattr(block, "cells"):
            print(f"  Table: {block.rows}x{block.columns}")
            for i, cell in enumerate(block.cells):
                print(f"    Cell {i}: {cell}")
