from document_client import get_document_intelligence_client
from document_models import ExtractedBlock, BoundingBox
from azure.ai.documentintelligence.models import DocumentAnalysisFeature


def extract_layout_from_document(document_path: str) -> list[ExtractedBlock]:
    client = get_document_intelligence_client()

    with open(document_path, "rb") as f:
        poller = client.begin_analyze_document(
            "prebuilt-layout",
            analyze_request=f,
            content_type="application/octet-stream",
        )
    result = poller.result()

    extracted_blocks = []
    for paragraph in result.paragraphs:
        if paragraph.bounding_regions:
            bounding_box = paragraph.bounding_regions[0].bounding_box
            extracted_blocks.append(
                ExtractedBlock(
                    content=paragraph.content,
                    bounding_box=BoundingBox(
                        x1=bounding_box[0].x,
                        y1=bounding_box[0].y,
                        x2=bounding_box[2].x,
                        y2=bounding_box[2].y,
                    ),
                    kind="paragraph",
                )
            )

    for table in result.tables:
        if table.bounding_regions:
            bounding_box = table.bounding_regions[0].bounding_box
            extracted_blocks.append(
                ExtractedBlock(
                    content="[TABLE]",  # Placeholder for table content
                    bounding_box=BoundingBox(
                        x1=bounding_box[0].x,
                        y1=bounding_box[0].y,
                        x2=bounding_box[2].x,
                        y2=bounding_box[2].y,
                    ),
                    kind="table",
                )
            )

    # Sort blocks by their Y-coordinate for a more natural reading order
    extracted_blocks.sort(key=lambda block: block.bounding_box.y1)

    return extracted_blocks
