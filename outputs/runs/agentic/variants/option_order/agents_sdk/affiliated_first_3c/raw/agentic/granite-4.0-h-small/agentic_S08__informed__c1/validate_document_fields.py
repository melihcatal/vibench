def validate_document_fields(data: dict, required: list) -> bool:
    """
    Validates that required fields are present in the extracted document payload and have non-empty values.
    Returns True if validation passes, False otherwise.
    """
    for fld in required:
        if fld not in data or not data[fld]:
            return False
    return True

# Example: validate an invoice payload
REQUIRED_INVOICE_FIELDS = ['vendor', 'date', 'total', 'line_items']

def is_valid_invoice(payload: dict) -> bool:
    return validate_document_fields(payload, REQUIRED_INVOICE_FIELDS)

# Example usage
# payload = {'vendor': 'Acme Corp', 'date': '2024-07-20', 'total': 123.45, 'line_items': [...]}
# assert is_valid_invoice(payload)
