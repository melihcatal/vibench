from typing import List
from azure.ai.documentintelligence import DocumentIntelligenceClient
from document_client import get_document_intelligence_client
from document_models import ExtractedBlock

def extract_layout_from_url(url: str) -> List[ExtractedBlock]:
    """
    Extracts layout elements (paragraphs) from a document at a given URL.

    Args:
        url: The URL of the document to analyze.

    Returns:
        A list of ExtractedBlock objects representing paragraphs.
    """
    document_intelligence_client = get_document_intelligence_client()
    
    poller = document_intelligence_client.begin_analyze_document(
        "prebuilt-layout", {"urlSource": url}
    )
    result = poller.result()

    blocks = []
    if result.paragraphs:
        for paragraph in result.paragraphs:
            blocks.append(
                ExtractedBlock(
                    role=paragraph.role,
                    content=paragraph.content,
                    bounding_box=[
                        (p.x, p.y) for p in paragraph.bounding_regions[0].polygon
                    ],
                )
            )
    return blocks
