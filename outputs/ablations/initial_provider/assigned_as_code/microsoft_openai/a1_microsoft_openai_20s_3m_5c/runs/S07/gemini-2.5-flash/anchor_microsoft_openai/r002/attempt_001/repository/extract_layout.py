import io
from document_client import get_document_intelligence_client
from document_models import AnalyzeDocumentRequest, DocumentLayout

def extract_layout(payload: AnalyzeDocumentRequest, config=None) -> DocumentLayout:
    client = get_document_intelligence_client(config)
    with client:
        poller = client.begin_analyze_document(
            "prebuilt-layout",
            body=io.BytesIO(payload.document_bytes),
            content_type=payload.mime_type
        )
        result = poller.result()

    return DocumentLayout(
        pages=[p.to_dict() for p in result.pages] if result.pages else [],
        tables=[t.to_dict() for t in result.tables] if result.tables else [],
        key_value_pairs=[kv.to_dict() for kv in result.key_value_pairs] if result.key_value_pairs else [],
        paragraphs=[p.to_dict() for p in result.paragraphs] if result.paragraphs else [],
        styles=[s.to_dict() for s in result.styles] if result.styles else [],
        languages=[l.to_dict() for l in result.languages] if result.languages else []
    )
