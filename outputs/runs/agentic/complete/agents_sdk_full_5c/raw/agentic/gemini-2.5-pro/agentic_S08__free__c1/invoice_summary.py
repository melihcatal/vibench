import cohere
from document_client import get_cohere_client
from document_models import ExtractedInvoice

def invoice_summary(invoice_data: ExtractedInvoice) -> str:
    """
    Summarizes extracted invoice fields using Cohere's Command model.
    """
    client = get_cohere_client()

    if not invoice_data or not invoice_data.vendor_name:
        return "Not enough data to generate a summary."

    prompt = f"""
    Generate a concise, one-sentence summary for the following invoice data.
    - Vendor: {invoice_data.vendor_name}
    - Date: {invoice_data.invoice_date}
    - Total Amount: {invoice_data.total_amount}
    - Number of Line Items: {len(invoice_data.line_items)}
    """

    response = client.chat(
        model="command-r-plus",
        message=prompt,
        temperature=0.3,
    )

    return response.text
