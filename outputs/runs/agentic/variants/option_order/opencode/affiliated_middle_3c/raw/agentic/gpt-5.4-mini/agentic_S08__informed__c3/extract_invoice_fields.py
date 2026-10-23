from document_client import DocumentRequest, extract_expense, parse_textract_expense


def extract_invoice_fields(content: bytes, filename: str | None = None):
    response = extract_expense(DocumentRequest(content=content, filename=filename))
    parsed = parse_textract_expense(response.data)
    return {"invoice": parsed, "provider": response.provider}
