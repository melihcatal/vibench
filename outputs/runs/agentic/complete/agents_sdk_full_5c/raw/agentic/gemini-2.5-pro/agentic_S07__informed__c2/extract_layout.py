
from document_client import get_document_intelligence_client
from document_models import DocumentFile, ExtractedLayout

def extract_layout_from_document(doc: DocumentFile) -> ExtractedLayout:
    """
    Extracts layout elements from a document image using Azure Document Intelligence.
    """
    client = get_document_intelligence_client()

    poller = None
    if doc.file_bytes:
        poller = client.begin_analyze_document(
            "prebuilt-layout",
            doc.file_bytes,
            content_type="application/octet-stream"
        )
    elif doc.file_url:
        poller = client.begin_analyze_document(
            "prebuilt-layout", {"urlSource": doc.file_url}
        )
    else:
        raise ValueError("DocumentFile must have file_bytes or file_url.")

    result = poller.result()
    
    return ExtractedLayout(
        pages=result.pages,
        paragraphs=result.paragraphs,
        raw_response=result
    )
