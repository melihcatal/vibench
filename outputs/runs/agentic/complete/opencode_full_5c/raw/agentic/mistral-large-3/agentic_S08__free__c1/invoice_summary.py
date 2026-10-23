from typing import Dict, Any
from document_models import InvoiceFields


def invoice_summary(extracted_data: Dict[str, Any]) -> str:
    invoice = InvoiceFields(**extracted_data)

    summary_lines = []
    summary_lines.append(f"Invoice Summary for {invoice.vendor or 'Unknown Vendor'}")
    summary_lines.append(f"Date: {invoice.date or 'Not specified'}")
    summary_lines.append(f"Total Amount: ${invoice.total:.2f}")
    summary_lines.append("\nLine Items:")

    if invoice.line_items:
        for item in invoice.line_items:
            description = item.description or "No description"
            amount = (
                item.amount or item.unit_price * item.quantity
                if (item.unit_price and item.quantity)
                else 0
            )
            summary_lines.append(f"- {description}: ${amount:.2f}")
    else:
        summary_lines.append("- No line items found")

    summary_lines.append(f"\nConfidence: {invoice.confidence * 100:.1f}%")
    return "\n".join(summary_lines)
