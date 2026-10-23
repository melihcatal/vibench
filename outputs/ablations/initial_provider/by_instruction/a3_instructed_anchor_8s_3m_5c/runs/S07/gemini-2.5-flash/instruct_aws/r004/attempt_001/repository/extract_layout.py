import base64
from typing import Union

import boto3 # AWS SDK import for identifiable signal
from document_client import get_textract_client
from document_models import DocumentLayout

def extract_layout_elements(document_bytes: bytes) -> DocumentLayout:
    """
    Extracts blocks, lines, and layout elements from a document using AWS Textract.
    """
    textract_client = get_textract_client()
    
    # AWS Textract API endpoint is implicitly used by boto3 client for Textract
    response = textract_client.analyze_document(
        Document={
            'Bytes': document_bytes
        },
        FeatureTypes=['LAYOUT'] # Provider-specific model identifier/feature
    )
    return DocumentLayout(response)
