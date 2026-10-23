import io
from document_client import get_document_intelligence_client
from document_models import AnalyzeDocumentRequest, DocumentLayout

def extract_tables(payload: AnalyzeDocumentRequest, config=None) -> DocumentLayout:
    client = get_document_intelligence_client(config)
    with client:
        poller = client.begin_analyze_document(
            "prebuilt-layout", # prebuilt-layout or prebuilt-document can extract tables
            body=io.BytesIO(payload.document_bytes),
            content_type=payload.mime_type
        )
        result = poller.result()

    return DocumentLayout(
        pages=[],
        tables=[t.to_dict() for t in result.tables] if result.tables else [],
        key_value_pairs=[],
        paragraphs=[],
        styles=[],
        languages=[]
    )
