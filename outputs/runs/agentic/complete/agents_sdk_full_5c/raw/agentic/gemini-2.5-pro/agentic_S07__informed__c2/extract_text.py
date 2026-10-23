
from document_client import get_document_intelligence_client
from document_models import DocumentFile, ExtractedText

def extract_text_from_document(doc: DocumentFile) -> ExtractedText:
    """
    Extracts plain text from a document image using Azure Document Intelligence.
    """
    client = get_document_intelligence_client()

    poller = None
    if doc.file_bytes:
        poller = client.begin_analyze_document(
            "prebuilt-read",
            doc.file_bytes,
            content_type="application/octet-stream"
        )
    elif doc.file_url:
        poller = client.begin_analyze_document(
            "prebuilt-read", {"urlSource": doc.file_url}
        )
    else:
        raise ValueError("DocumentFile must have file_bytes or file_url.")

    result = poller.result()
    
    return ExtractedText(
        content=result.content,
        raw_response=result
    )
