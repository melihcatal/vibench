from document_client import get_document_client
from document_models import AnalyzeResult


def extract_text(document_stream: bytes) -> AnalyzeResult:
    client = get_document_client()
    poller = client.begin_analyze_document(
        "prebuilt-read", document_stream, content_type="application/octet-stream"
    )
    result = poller.result()

    # Azure AI Document Intelligence uses 'content' for plain text
    # We'll populate a basic AnalyzeResult with the content and lines
    lines = []
    if result.pages:
        for page in result.pages:
            if page.lines:
                for line in page.lines:
                    lines.append(
                        {
                            "content": line.content,
                            "bounding_regions": [
                                r.to_dict() for r in line.bounding_regions
                            ]
                            if line.bounding_regions
                            else [],
                            "spans": [s.to_dict() for s in line.spans]
                            if line.spans
                            else [],
                        }
                    )

    return AnalyzeResult(
        pages=[p.to_dict() for p in result.pages] if result.pages else [],
        paragraphs=[p.to_dict() for p in result.paragraphs]
        if result.paragraphs
        else [],
        lines=lines,
        words=[w.to_dict() for w in result.words] if result.words else [],
        tables=[],
        key_value_pairs=[],
        styles=[s.to_dict() for s in result.styles] if result.styles else [],
        languages=[l.to_dict() for l in result.languages] if result.languages else [],
        documents=[d.to_dict() for d in result.documents] if result.documents else [],
        content=result.content if result.content else "",
    )
