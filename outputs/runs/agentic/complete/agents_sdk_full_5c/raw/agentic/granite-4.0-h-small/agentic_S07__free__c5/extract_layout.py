import os
from document_client import DocumentClient
from document_models import LayoutResponse

def extract_layout(image_path: str) -> dict:
    """Extract blocks, lines, tables, or layout elements from a document using AWS Textract layout analysis.
    
    Returns a dict representing the hierarchical layout structure.
    """
    client = DocumentClient()  # uses AWS credentials from env vars
    response = client.start_layout_detection(image_path)
    # Poll for completion (simplified)
    layout = client.get_layout_result(response["JobId"])
    return layout
