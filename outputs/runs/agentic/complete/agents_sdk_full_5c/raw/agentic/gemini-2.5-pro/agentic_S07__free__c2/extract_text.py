
from typing import Union
from document_client import get_document_client
from document_models import ExtractedText

def extract_text_from_document(file_source: Union[bytes, str]) -> ExtractedText:
    """
    Extracts plain text from a document image or URL using Azure AI Document Intelligence.

    Args:
        file_source: A byte string containing the document content, or a URL string.
    """
    client = get_document_client()

    poller_args = {}
    if isinstance(file_source, bytes):
        poller_args["analyze_request"] = file_source
        poller_args["content_type"] = "application/octet-stream"
    elif isinstance(file_source, str):
        poller_args["url_source"] = file_source
    else:
        raise TypeError("file_source must be bytes or a URL string.")

    poller = client.begin_analyze_document(
        "prebuilt-read",
        **poller_args
    )
    result = poller.result()

    return ExtractedText(content=result.content)
