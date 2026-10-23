from document_client import get_document_client
from document_models import AnalyzeResult, DocumentTable


def extract_tables(document_stream: bytes) -> AnalyzeResult:
    client = get_document_client()
    poller = client.begin_analyze_document(
        "prebuilt-layout", document_stream, content_type="application/octet-stream"
    )
    result = poller.result()

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
        pages=[p.to_dict() for p in result.pages] if result.pages else [],
        paragraphs=[p.to_dict() for p in result.paragraphs]
        if result.paragraphs
        else [],
        lines=[l.to_dict() for l in result.lines] if result.lines else [],
        words=[w.to_dict() for w in result.words] if result.words else [],
        tables=tables,
        key_value_pairs=[],
        styles=[s.to_dict() for s in result.styles] if result.styles else [],
        languages=[l.to_dict() for l in result.languages] if result.languages else [],
        documents=[d.to_dict() for d in result.documents] if result.documents else [],
        content=result.content if result.content else "",
    )
