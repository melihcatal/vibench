from document_client import analyze_document, get_result_content
from document_models import normalize_key_values


def extract_key_values(source_url=None, source_bytes=None):
    result = analyze_document(
        "prebuilt-document", source_url=source_url, source_bytes=source_bytes
    )
    content = get_result_content(result)
    return normalize_key_values(content.get("documents", []))
