from document_client import make_client, load_config
from document_models import DocumentRequest, normalize_analyze_result


def extract_tables(document: DocumentRequest):
    client = make_client()
    config = load_config()
    poller = client.begin_analyze_document(
        config.model_id, document.content, content_type=document.content_type
    )
    result = poller.result()
    return normalize_analyze_result(result).tables
