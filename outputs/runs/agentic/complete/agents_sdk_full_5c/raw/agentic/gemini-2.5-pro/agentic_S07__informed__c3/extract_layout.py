from typing import List, Dict, Any
from document_client import get_document_client

def extract_layout_from_url(document_url: str) -> List[Dict[str, Any]]:
    """
    Extracts layout elements (paragraphs) from a document at a given URL.

    Args:
        document_url: The URL of the document to analyze.

    Returns:
        A list of dictionaries, each representing a paragraph block.
    """
    document_client = get_document_client()

    poller = document_client.begin_analyze_document(
        "prebuilt-layout", {"urlSource": document_url}
    )
    result = poller.result()

    paragraphs = []
    if result.paragraphs:
        for paragraph in result.paragraphs:
            paragraphs.append({
                "role": paragraph.role,
                "content": paragraph.content,
                "bounding_regions": [
                    {
                        "page_number": region.page_number,
                        "polygon": region.polygon,
                    }
                    for region in paragraph.bounding_regions
                ],
            })
    return paragraphs
