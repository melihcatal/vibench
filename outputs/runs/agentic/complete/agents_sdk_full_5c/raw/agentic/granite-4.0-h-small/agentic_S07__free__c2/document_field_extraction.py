import re
from .document_models import KeyValueResult

def document_field_extraction(kv_result: KeyValueResult) -> dict:
    """Extract structured fields (e.g., Name, Date, Amount) from key‑value pairs.",
    """
    # Simple regex‑based extraction; replace with domain‑specific logic as needed
    fields = {}
    for pair in kv_result['pairs']:
        key = pair.get('key', '').strip().lower()
        value = pair.get('value', '').strip()
        if key in ['name', 'full name']:
            fields['Name'] = value
        elif key in ['date', 'date issued']:
            fields['Date'] = value
        elif key in ['amount', 'total']:
            fields['Amount'] = value
    return fields
