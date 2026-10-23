from document_client import analyze_document, get_result_content
from document_models import normalize_document_response


def extract_layout(source_url=None, source_bytes=None):
    result = analyze_document(
        "prebuilt-layout", source_url=source_url, source_bytes=source_bytes
    )
    return normalize_document_response(get_result_content(result))
