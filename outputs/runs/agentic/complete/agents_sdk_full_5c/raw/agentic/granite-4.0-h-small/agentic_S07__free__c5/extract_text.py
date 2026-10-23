import os
from document_client import DocumentClient
from document_models import OcrResponse

def extract_text(image_path: str) -> str:
    """Extract plain text from a scanned document image using AWS Textract.
    
    Returns the concatenated plain text.
    """
    client = DocumentClient()  # uses AWS credentials from env vars
    response = client.start_text_detection(image_path)
    # Poll for completion (simplified)
    text = client.get_text_detection_result(response["JobId"])
    return text
