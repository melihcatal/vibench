def normalize_expense(extracted):
    """
    Convert vendor/receipt extraction payloads into a standard JSON schema:
    {
        'vendor_or_merchant': str,
        'date': str or None,
        'total': float or None,
        'line_items_or_items': List[dict],
        'confidence': float or None
    }
    """
    normalized = {
        'vendor_or_merchant': extracted.get('vendor') or extracted.get('merchant'),
        'date': extracted.get('date'),
        'total': extracted.get('total'),
        'line_items_or_items': extracted.get('line_items') or extracted.get('items'),
        'confidence': extracted.get('confidence')
    }
    return normalized