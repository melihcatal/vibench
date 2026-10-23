from document_client import get_document_client
from document_models import LayoutBlock
from azure.ai.documentintelligence.models import AnalyzeResult
from typing import List

def extract_layout_from_url(document_url: str) -> List[LayoutBlock]:
    """
    Extracts layout elements (paragraphs, titles, etc.) from a document at a URL.
    
    Args:
        document_url: The URL of the document to analyze.
        
    Returns:
        A list of LayoutBlock objects representing the document structure.
    """
    client = get_document_client()
    
    poller = client.begin_analyze_document_from_url(
        model_id="prebuilt-layout",
        url=document_url
    )
    result: AnalyzeResult = poller.result()
    
    extracted_blocks = []
    if result.paragraphs:
        for paragraph in result.paragraphs:
            bounding_box = [
                {"x": p.x, "y": p.y} for p in paragraph.bounding_regions[0].polygon
            ]
            block = LayoutBlock(
                kind=paragraph.role if paragraph.role else "paragraph",
                content=paragraph.content,
                bounding_box=bounding_box
            )
            extracted_blocks.append(block)
            
    return extracted_blocks
