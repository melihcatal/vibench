import os
import cohere
from document_models import Invoice, Summary


def invoice_summary(invoice: Invoice) -> Summary:
    """
    Summarizes extracted invoice fields using Cohere.
    """
    co = cohere.Client(os.getenv("COHERE_API_KEY"))

    line_items_str = "\n".join(
        [
            f"- {item.description} (Qty: {item.quantity}, "
            f"Unit Price: ${item.unit_price}, Total: ${item.total_amount})"
            for item in invoice.line_items
        ]
    )

    prompt = f"""
    Summarize the following invoice:

    Vendor: {invoice.vendor_name}
    Date: {invoice.invoice_date}
    Total Amount: ${invoice.total_amount}

    Line Items:
    {line_items_str}

    Provide a brief, one-sentence summary of this invoice.
    """

    response = co.summarize(
        text=prompt, model="command", length="short", extractiveness="low"
    )

    summary_text = response.summary
    return Summary(summary_text=summary_text)
