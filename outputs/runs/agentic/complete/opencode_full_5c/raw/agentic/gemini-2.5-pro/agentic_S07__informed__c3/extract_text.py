from document_client import get_document_analysis_client


def extract_text_from_document(file_path: str = None, url: str = None):
    """
    Extracts text from a document using Azure Document Intelligence.
    """
    client = get_document_analysis_client()

    poller = None
    if url:
        poller = client.begin_analyze_document("prebuilt-read", {"urlSource": url})
    elif file_path:
        with open(file_path, "rb") as f:
            poller = client.begin_analyze_document("prebuilt-read", f.read())
    else:
        raise ValueError("Either file_path or url must be provided.")

    result = poller.result()

    return result.content if result.content else ""
