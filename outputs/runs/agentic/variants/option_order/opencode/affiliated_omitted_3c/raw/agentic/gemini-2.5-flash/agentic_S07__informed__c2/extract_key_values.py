from document_client import get_document_client
from document_models import AnalyzeResult, DocumentKeyValuePair, DocumentTextLine


def extract_key_values(document_stream: bytes) -> AnalyzeResult:
    client = get_document_client()
    poller = client.begin_analyze_document(
        "prebuilt-document", document_stream, content_type="application/octet-stream"
    )
    result = poller.result()

    key_value_pairs = []
    if result.key_value_pairs:
        for kvp in result.key_value_pairs:
            key_value_pairs.append(
                DocumentKeyValuePair(
                    key=DocumentTextLine(
                        content=kvp.key.content,
                        bounding_regions=[r.to_dict() for r in kvp.key.bounding_regions]
                        if kvp.key.bounding_regions
                        else [],
                        spans=[s.to_dict() for s in kvp.key.spans]
                        if kvp.key.spans
                        else [],
                    ),
                    value=DocumentTextLine(
                        content=kvp.value.content,
                        bounding_regions=[
                            r.to_dict() for r in kvp.value.bounding_regions
                        ]
                        if kvp.value.bounding_regions
                        else [],
                        spans=[s.to_dict() for s in kvp.value.spans]
                        if kvp.value.spans
                        else [],
                    )
                    if kvp.value
                    else None,
                    confidence=kvp.confidence,
                )
            )

    return AnalyzeResult(
        pages=[p.to_dict() for p in result.pages] if result.pages else [],
        paragraphs=[p.to_dict() for p in result.paragraphs]
        if result.paragraphs
        else [],
        lines=[l.to_dict() for l in result.lines] if result.lines else [],
        words=[w.to_dict() for w in result.words] if result.words else [],
        tables=[t.to_dict() for t in result.tables] if result.tables else [],
        key_value_pairs=key_value_pairs,
        styles=[s.to_dict() for s in result.styles] if result.styles else [],
        languages=[l.to_dict() for l in result.languages] if result.languages else [],
        documents=[d.to_dict() for d in result.documents] if result.documents else [],
        content=result.content if result.content else "",
    )
