import os
from mindee import MindeeClient
from mindee.product import InvoiceV4

def extract_key_values(image_path: str) -> list[dict[str, str]]:
    api_key = os.getenv('MINDEE_API_KEY')
    client = MindeeClient(api_key)
    result = client.parse(InvoiceV4, image_path)
    prediction = result.document.inference.prediction
    kv_pairs = []
    fields = [
        ('supplier_name', prediction.supplier_name.value if hasattr(prediction, 'supplier_name') else None),
        ('invoice_number', prediction.invoice_number.value if hasattr(prediction, 'invoice_number') else None),
        ('total_amount', str(prediction.total_amount.value) if hasattr(prediction, 'total_amount') else None),
        ('date', prediction.due_date.value if hasattr(prediction, 'due_date') else None),
    ]
    for key, value in fields:
        if value:
            kv_pairs.append({'key': key, 'value': str(value)})
    return kv_pairs
