import os
from typing import Dict, Any
from document_models import ExtractedReceipt
from mindee import Mindee
from mindee.product import receipt

def extract_receipt_fields(file_path: str) -> ExtractedReceipt:
    mindee_client = Mindee(api_key=os.getenv('MINDEE_API_KEY'))
    result = mindee_client.parse(receipt.Receipt.V4, input_path=file_path)
    prediction = result.document.inference.prediction
    items: List[Dict[str, Any]] = []
    for supply in prediction.supplies:
        items.append({
            'description': supply.description.value if hasattr(supply.description, 'value') else '',
            'amount': supply.total_amount.value
        })
    conf: Dict[str, float] = {
        'merchant': prediction.supplier.confidence,
        'total': prediction.total_amount.confidence
    }
    tax_amount = sum([t.total_amount.value for t in prediction.taxes]) if prediction.taxes else None
    return ExtractedReceipt(
        merchant=prediction.supplier.value,
        tax=tax_amount,
        total=prediction.total_amount.value,
        items=items,
        confidence=conf
    )
