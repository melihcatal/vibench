from document_client import get_document_client
from document_models import ExtractedLayout, Block, Line


def extract_layout_from_document(file_path: str) -> ExtractedLayout:
    """
    Extracts layout elements (blocks, lines) from a document.
    """
    document_intelligence_client = get_document_client()

    with open(file_path, "rb") as f:
        poller = document_intelligence_client.begin_analyze_document(
            "prebuilt-layout",
            analyze_request=f,
            content_type="application/octet-stream",
        )
    result = poller.result()

    blocks = []
    if result.paragraphs:
        for paragraph in result.paragraphs:
            bounding_box = []
            if paragraph.bounding_regions:
                for region in paragraph.bounding_regions:
                    bounding_box.extend(region.polygon)
            blocks.append(Block(content=paragraph.content, bounding_box=bounding_box))

    lines = []
    if result.pages:
        for page in result.pages:
            if page.lines:
                for line in page.lines:
                    lines.append(Line(content=line.content, bounding_box=line.polygon))

    return ExtractedLayout(blocks=blocks, lines=lines)
