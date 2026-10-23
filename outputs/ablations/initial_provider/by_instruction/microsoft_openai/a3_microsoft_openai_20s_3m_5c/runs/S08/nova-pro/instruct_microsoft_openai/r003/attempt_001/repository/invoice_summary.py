from.extract_invoice_fields import extract_invoice_fields

def summarize_invoice(document_path: str):
    expense = extract_invoice_fields(document_path)
    return f'Invoice from {expense.vendor} on {expense.date} for a total of {expense.total} with {len(expense.items)} items'