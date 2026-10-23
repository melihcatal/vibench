import os
from document_client import DocumentClient
from document_models import KeyValueCollection

def extract_key_values(image_path: str) -> KeyValueCollection:
    """Extract key-value pairs from a form-like document using AWS Textract forms analysis.
    
    Returns a KeyValueCollection object containing matched keys and values.
    """
    client = DocumentClient()  # uses AWS credentials from env vars
    response = client.start_form_extraction(image_path)
    # Poll for completion (simplified)
    key_values = client.get_form_result(response["JobId"])
    return key_values
