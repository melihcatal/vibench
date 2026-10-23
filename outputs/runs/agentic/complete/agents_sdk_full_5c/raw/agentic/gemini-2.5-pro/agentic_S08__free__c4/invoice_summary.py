# invoice_summary.py
from document_client import get_cohere_client
from document_models import ExtractedInvoice

def summarize_invoice(invoice: ExtractedInvoice, length: str = "short") -> str:
    """
    Summarizes extracted invoice fields using the Cohere Summarize API.
    
    Args:
        invoice: The extracted invoice data.
        length: The desired summary length ('short', 'medium', 'long').
    
    Returns:
        A text summary of the invoice.
    """
    client = get_cohere_client()
    
    text_to_summarize = f"""
    Invoice from {invoice.vendor_name or 'N/A'}.
    Invoice ID: {invoice.invoice_id or 'N/A'}.
    Date: {invoice.invoice_date or 'N/A'}.
    Total Amount Due: {invoice.total_amount or 'N/A'}.
    """
    
    if invoice.line_items:
        text_to_summarize += "\nLine Items:\n"
        for item in invoice.line_items:
            text_to_summarize += f"- {item.description or 'Item'}: {item.total_price or 'N/A'}\n"

    response = client.summarize(
        text=text_to_summarize,
        length=length,
        format="paragraph",
        model="command-r-plus", 
    )
    
    return response.summary
