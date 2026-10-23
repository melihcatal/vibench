import json
from typing import Dict

def normalize_expense(extracted: dict) -> dict:
    """Convert extracted invoice or receipt fields to a standard expense schema.

    Expected input keys: vendor, date, total, line_items or items, tax
    Output schema:
    {
        "expenseId": str,
        "vendor": str,
        "date": str,
        "totalAmount": float,
        "lineItems": List[Dict[str, str]],
        "taxAmount": Optional[float],
        "confidence": float
    }
    """
    confidence = max(
        *[block.get('confidence', 0) for block in extracted.values() if isinstance(block, dict)],
        default=0
    )
    line_items = []
    if 'line_items' in extracted:
        for li in extracted['line_items']:
            line_items.extend(li.get('items', []))
    elif 'items' in extracted:
        line_items = extracted['items']
    return {
        "expenseId": str(hash(json.dumps(extracted))),
        "vendor": extracted.get('vendor', {}).get('text', ''),
        "date": extracted.get('date', {}).get('text', ''),
        "totalAmount": float(extracted.get('total', {}).get('text', '0')), 
        "lineItems": [
            {"description": item['text'], "amount": "0"} for item in line_items
        ],
        "taxAmount": float(extracted.get('tax', {}).get('text', '0')), 
        "confidence": confidence
    }
