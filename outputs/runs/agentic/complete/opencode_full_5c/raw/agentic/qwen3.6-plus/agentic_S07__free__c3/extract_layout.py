from document_client import get_azure_document_client
from document_models import (
    LayoutResponse,
    OcrBlock,
    OcrLine,
    OcrWord,
    BoundingBox,
    normalize_bounding_box,
    normalize_confidence,
)

AZURE_LAYOUT_MODEL_ID = "prebuilt-layout"


def extract_layout_from_document(
    document_bytes: bytes,
    content_type: str = "application/pdf",
) -> LayoutResponse:
    client = get_azure_document_client()

    poller = client.begin_analyze_document(
        AZURE_LAYOUT_MODEL_ID,
        document=document_bytes,
        content_type=content_type,
    )
    result = poller.result()

    blocks = []
    lines = []
    words = []

    for page in result.pages:
        for line in page.lines:
            line_words = []
            if line.words:
                for word in line.words:
                    bbox = _parse_azure_polygon(wordpolygon=word.polygon)
                    w = OcrWord(
                        text=word.content,
                        confidence=normalize_confidence(word.confidence),
                        bounding_box=bbox,
                    )
                    line_words.append(w)
                    words.append(w)

            line_bbox = _parse_azure_polygon(linepolygon=line.polygon)
            ocr_line = OcrLine(
                text=line.content,
                words=line_words,
                confidence=normalize_confidence(line.confidence),
                bounding_box=line_bbox,
            )
            lines.append(ocr_line)

        if page.selection_marks:
            for mark in page.selection_marks:
                bbox = _parse_azure_polygon(markpolygon=mark.polygon)
                block = OcrBlock(
                    block_type="selectionMark",
                    text="selected" if mark.state.value == "selected" else "unselected",
                    confidence=normalize_confidence(mark.confidence),
                    bounding_box=bbox,
                )
                blocks.append(block)

        if page.tables:
            for table in page.tables:
                bbox = _parse_azure_polygon(tablepolygon=table.polygon)
                block = OcrBlock(
                    block_type="table",
                    text=f"Table {table.row_count}x{table.column_count}",
                    confidence=normalize_confidence(table.confidence),
                    bounding_box=bbox,
                )
                blocks.append(block)

    page_width = 1.0
    page_height = 1.0
    if result.pages:
        first_page = result.pages[0]
        page_width = first_page.width
        page_height = first_page.height

    return LayoutResponse(
        blocks=blocks,
        lines=lines,
        page_width=page_width,
        page_height=page_height,
    )


def extract_layout_from_url(
    document_url: str,
) -> LayoutResponse:
    client = get_azure_document_client()

    poller = client.begin_analyze_document_from_url(
        AZURE_LAYOUT_MODEL_ID,
        document_url=document_url,
    )
    result = poller.result()

    blocks = []
    lines = []

    for page in result.pages:
        for line in page.lines:
            line_words = []
            if line.words:
                for word in line.words:
                    bbox = _parse_azure_polygon(wordpolygon=word.polygon)
                    w = OcrWord(
                        text=word.content,
                        confidence=normalize_confidence(word.confidence),
                        bounding_box=bbox,
                    )
                    line_words.append(w)

            line_bbox = _parse_azure_polygon(linepolygon=line.polygon)
            ocr_line = OcrLine(
                text=line.content,
                words=line_words,
                confidence=normalize_confidence(line.confidence),
                bounding_box=line_bbox,
            )
            lines.append(ocr_line)

    page_width = 1.0
    page_height = 1.0
    if result.pages:
        first_page = result.pages[0]
        page_width = first_page.width
        page_height = first_page.height

    return LayoutResponse(
        blocks=blocks,
        lines=lines,
        page_width=page_width,
        page_height=page_height,
    )


def _parse_azure_polygon(
    polygon=None,
    wordpolygon=None,
    linepolygon=None,
    markpolygon=None,
    tablepolygon=None,
):
    poly = polygon or wordpolygon or linepolygon or markpolygon or tablepolygon or []
    if not poly:
        return BoundingBox(x=0.0, y=0.0, width=0.0, height=0.0)
    points = [(p.x, p.y) for p in poly]
    return normalize_bounding_box(points)
