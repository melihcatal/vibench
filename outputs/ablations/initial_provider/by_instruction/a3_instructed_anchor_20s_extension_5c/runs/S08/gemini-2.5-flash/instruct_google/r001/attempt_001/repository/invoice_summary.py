from document_models import Invoice

def summarize_invoice(invoice: Invoice) -> str:
    summary_parts = []
    summary_parts.append("--- Invoice Summary ---")
    if invoice.vendor_name:
        summary_parts.append(f"Vendor: {invoice.vendor_name}")
    if invoice.invoice_date:
        summary_parts.append(f"Date: {invoice.invoice_date}")
    if invoice.total_amount is not None:
        summary_parts.append(f"Total Amount: ${invoice.total_amount:.2f}")

    if invoice.line_items:
        summary_parts.append("Line Items:")
        for item in invoice.line_items:
            item_summary = f"  - {item.description}"
            if item.quantity is not None:
                item_summary += f" (Qty: {item.quantity})
            if item.unit_price is not None:
                item_summary += f" (Unit Price: ${item.unit_price:.2f})
            if item.total_price is not None:
                item_summary += f" (Total: ${item.total_price:.2f})
            summary_parts.append(item_summary)
    
    if not summary_parts:
        return "No significant invoice details to summarize."

    return "\n".join(summary_parts)
