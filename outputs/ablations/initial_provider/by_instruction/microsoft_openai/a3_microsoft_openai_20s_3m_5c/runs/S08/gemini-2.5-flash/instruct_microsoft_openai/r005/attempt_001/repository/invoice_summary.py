from typing import Optional
from document_client import get_openai_client, call_openai_chat_model
from document_models import InvoiceFields

def summarize_invoice(invoice_fields: InvoiceFields, model_deployment_name: str = "gpt-4o") -> Optional[str]:
    """
    Summarizes extracted invoice fields using Azure OpenAI.
    """
    client = get_openai_client()

    summary_prompt = f"""
    Summarize the following invoice details in a concise paragraph, highlighting the vendor, total amount, and key line items.

    Invoice Details:
    Vendor: {invoice_fields.vendor_name if invoice_fields.vendor_name else 'N/A'}
    Date: {invoice_fields.invoice_date if invoice_fields.invoice_date else 'N/A'}
    Total Amount: {invoice_fields.total_amount if invoice_fields.total_amount is not None else 'N/A'}
    Line Items:
    {'; '.join([f'{item.description} (Qty: {item.quantity}, Price: {item.unit_price})' for item in invoice_fields.line_items]) if invoice_fields.line_items else 'N/A'}
    """

    try:
        summary_text = call_openai_chat_model(client, model_deployment_name, summary_prompt, temperature=0.5)
        return summary_text
    except Exception as e:
        print(f"Error summarizing invoice: {e}")
        return None
