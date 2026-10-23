import os
from mindee import Client
from mindee.product.invoice import InvoiceV4
from document_models import KeyValuePair
from typing import Dict, List
from document_client import load_document_image

def extract_key_values(image_path: str) -> Dict[str, str]:
    """
    Extract key-value pairs from form-like document using Mindee Invoice OCR.
    """
    api_key = os.getenv('MINDEE_API_KEY')
    client = Client(api_key=api_key)

    with open(image_path, 'rb') as fp:
        result = client.load(InvoiceV4, fp).parse()

    prediction = result.document.inference.prediction
    kv_pairs: Dict[str, str] = {}
    field_mapping = {
        'supplier': prediction.supplier.company_name.value if prediction.supplier.company_name else None,
        'date': prediction.date.value if prediction.date else None,
        'invoice_number': prediction.invoice_number.value if prediction.invoice_number else None,
        'total_amount': prediction.total_amount.value if prediction.total_amount else None,
        'tax_amount': prediction.tax_amount.value if prediction.tax_amount else None,
    }
    for key, value in field_mapping.items():
        if value:
            kv_pairs[key] = str(value)

    return kv_pairs
