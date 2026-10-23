# extract_text.py
from document_client import get_document_intelligence_client
from document_models import ExtractedText

def extract_text_from_url(document_url: str) -> ExtractedText:
    """
    Extracts plain text from a document image using Azure AI Document Intelligence.
    This uses the "prebuilt-read" model for high-quality OCR.
    """
    client = get_document_intelligence_client()
    
    poller = client.begin_analyze_document(
        "prebuilt-read", analyze_request={"urlSource": document_url}
    )
    result = poller.result()

    extracted_content = ""
    if result.content:
        extracted_content = result.content

    return ExtractedText(content=extracted_content, source_url=document_url)
