import boto3
from typing import Dict, Any
from document_client import parse_textract_expense

def extract_invoice_fields(image_bytes: bytes) -> Dict[str, Any]:
    client = boto3.client('textract')
    response = client.analyze_expense(
        Document={'Bytes': image_bytes},
        FeatureTypes=['INVOICES']
    )
    return parse_textract_expense(response)
