from document_client import analyze_document, get_result_content


def extract_text(source_url=None, source_bytes=None):
    result = analyze_document(
        "prebuilt-read", source_url=source_url, source_bytes=source_bytes
    )
    content = get_result_content(result)
    return content.get("content", "")
