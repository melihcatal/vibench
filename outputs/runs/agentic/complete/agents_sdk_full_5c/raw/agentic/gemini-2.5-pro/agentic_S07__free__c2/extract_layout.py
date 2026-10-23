
from typing import List, Union
from document_client import get_document_client
from document_models import LayoutElement

def extract_layout_from_document(file_source: Union[bytes, str]) -> List[LayoutElement]:
    """
    Extracts layout elements (paragraphs, titles, etc.) from a document image or URL
    using Azure AI Document Intelligence.

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
        "prebuilt-layout",
        **poller_args
    )
    result = poller.result()

    layout_elements = []
    if result.paragraphs:
        for para in result.paragraphs:
            bounding_box = [
                (point.x, point.y) for point in para.bounding_regions[0].polygon
            ] if para.bounding_regions else []
            layout_elements.append(
                LayoutElement(
                    content=para.content,
                    bounding_box=bounding_box,
                    role=para.role,
                )
            )

    return layout_elements
