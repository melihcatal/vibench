from document_models import NormalizedExpense
import json

def summarize_invoice(normalized: NormalizedExpense) -> str:
    """Create a concise readable summary of an invoice.
    Example output:
    Invoice for Acme Corp dated 2024-07-15 totaling $1,250.00
    Items:
      Widget A x 5 @ $100.00 each
      Widget B x 2 @ $75.00 each
    """
    lines = []
    lines.append(
        f"Invoice for {normalized.vendor_or_merchant} dated {normalized.date} totaling {normalized.total}"
    )
    if normalized.items:
        lines.append("Items:")
        for it in normalized.items:
            # Prefer price; fall back to quantity+unit_price
            if 'price' in it:
                lines.append(f"  {it['description']} @ ${it['price']}")
            else:
                qty = it.get('quantity', '')
                unit = it.get('unit_price', '')
                lines.append(f"  {it['description']} x {qty} @ ${unit} each")
    return "\n".join(lines)
