import json

def invoice_summary(expense_record):
    """
    Generate a concise human‑readable summary of an invoice expense record.
    expense_record: dict conforming to NormalizedExpense schema.
    Returns a formatted string.
    """
    lines = []
    lines.append(f"Vendor: {expense_record['vendor']}")
    lines.append(f"Date: {expense_record['date']}")
    lines.append(f"Total: ${expense_record['amount']:.2f} {expense_record['currency']}" )
    lines.append(f"Currency: {expense_record['currency']}" )
    items = expense_record.get('line_items', [])
    if items:
        lines.append("Line Items:")
        for i, it in enumerate(items, 1):
            lines.append(f"  {i}. {it['description']} - ${it['price']:.2f} x {it.get('quantity', 1)} = ${it['price'] * it.get('quantity', 1):.2f}")
    else:
        lines.append("No line items found.")
    return "\\n".join(lines)
