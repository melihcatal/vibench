import io
from document_client import get_document_intelligence_client
from document_models import AnalyzeDocumentRequest, DocumentLayout

def extract_key_values(payload: AnalyzeDocumentRequest, config=None) -> DocumentLayout:
    client = get_document_intelligence_client(config)
    with client:
        poller = client.begin_analyze_document(
            "prebuilt-document", # prebuilt-document is good for key-value pairs
            body=io.BytesIO(payload.document_bytes),
            content_type=payload.mime_type
        )
        result = poller.result()

    return DocumentLayout(
        pages=[],
        tables=[],
        key_value_pairs=[kv.to_dict() for kv in result.key_value_pairs] if result.key_value_pairs else [],
        paragraphs=[],
        styles=[],
        languages=[]
    )
