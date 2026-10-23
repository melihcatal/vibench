import json
from document_models import NormalizedExpense


def summarize_invoice(normalized: NormalizedExpense) -> str:
    """Creates a concise human-readable summary of an extracted invoice.","""
    lines = [
        f"Vendor: {normalized['vendor']}",
        f"Date: {normalized['date']}",
        f"Total: {normalized['total']:.2f}",
    ]
    line_items = normalized["line_items"]
    if line_items:
        lines.append("Line Items:")
        for i, li in enumerate(line_items, 1):
            lines.append(
                f"  [#{i}] {li['description']} - {li['quantity']} x {li['unit_price']:.2f} = {li['total']:.2f}"
            )
    else:
        lines.append("No line items found.")
    return "\n".join(lines)
