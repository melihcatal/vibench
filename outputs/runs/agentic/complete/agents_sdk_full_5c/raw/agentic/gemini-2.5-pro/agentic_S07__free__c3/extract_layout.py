from azure.ai.documentintelligence.models import AnalyzeResult
from document_client import get_azure_document_intelligence_client
from document_models import BoundingBox, Point, Line
from typing import List

def extract_layout_from_document(document_path: str) -> List[Line]:
    """
    Extracts layout elements (lines) from a document using Azure AI Document Intelligence.
    
    Args:
        document_path: The local path to the document file (e.g., PDF, PNG).

    Returns:
        A list of Line objects representing the document's layout.
    """
    document_intelligence_client = get_azure_document_intelligence_client()
    
    with open(document_path, "rb") as f:
        poller = document_intelligence_client.begin_analyze_document(
            "prebuilt-layout", analyze_request=f, content_type="application/octet-stream"
        )
    result: AnalyzeResult = poller.result()

    extracted_lines: List[Line] = []
    if result.pages:
        for page in result.pages:
            for line in page.lines:
                points = [Point(x=p.x, y=p.y) for p in line.polygon]
                bounding_box = BoundingBox(points=points)
                extracted_lines.append(
                    Line(
                        text=line.content,
                        bounding_box=bounding_box,
                        confidence=line.confidence
                    )
                )

    return extracted_lines
