from document_client import get_document_client
from document_models import (
    AnalyzeResult,
    DocumentBlock,
    DocumentTextLine,
    DocumentPage,
    DocumentTable,
    DocumentKeyValuePair,
)


def extract_layout(document_stream: bytes) -> AnalyzeResult:
    client = get_document_client()
    poller = client.begin_analyze_document(
        "prebuilt-layout", document_stream, content_type="application/octet-stream"
    )
    result = poller.result()

    pages = []
    if result.pages:
        for page in result.pages:
            pages.append(
                DocumentPage(
                    page_number=page.page_number,
                    width=page.width,
                    height=page.height,
                    unit=page.unit,
                )
            )

    lines = []
    if result.pages:
        for page in result.pages:
            if page.lines:
                for line in page.lines:
                    lines.append(
                        DocumentTextLine(
                            content=line.content,
                            bounding_regions=[
                                r.to_dict() for r in line.bounding_regions
                            ]
                            if line.bounding_regions
                            else [],
                            spans=[s.to_dict() for s in line.spans]
                            if line.spans
                            else [],
                        )
                    )

    # Document Intelligence SDK directly provides paragraphs as content blocks.
    # For this model, we'll map paragraphs to generic DocumentBlock.
    blocks = []
    if result.paragraphs:
        for paragraph in result.paragraphs:
            blocks.append(
                DocumentBlock(
                    content=paragraph.content,
                    bounding_regions=[r.to_dict() for r in paragraph.bounding_regions]
                    if paragraph.bounding_regions
                    else [],
                    spans=[s.to_dict() for s in paragraph.spans]
                    if paragraph.spans
                    else [],
                    kind="paragraph",
                )
            )

    tables = []
    if result.tables:
        for table in result.tables:
            tables.append(
                DocumentTable(
                    row_count=table.row_count,
                    column_count=table.column_count,
                    bounding_regions=[r.to_dict() for r in table.bounding_regions]
                    if table.bounding_regions
                    else [],
                    spans=[s.to_dict() for s in table.spans] if table.spans else [],
                    cells=[c.to_dict() for c in table.cells] if table.cells else [],
                )
            )

    return AnalyzeResult(
        pages=pages,
        paragraphs=[p.to_dict() for p in result.paragraphs]
        if result.paragraphs
        else [],
        lines=lines,
        words=[w.to_dict() for w in result.words] if result.words else [],
        tables=tables,
        key_value_pairs=[],
        styles=[s.to_dict() for s in result.styles] if result.styles else [],
        languages=[l.to_dict() for l in result.languages] if result.languages else [],
        documents=[d.to_dict() for d in result.documents] if result.documents else [],
        content=result.content if result.content else "",
    )
