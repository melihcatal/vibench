from document_client import get_openai_client
from document_models import ExtractedInvoice


def summarize_invoice(invoice: ExtractedInvoice) -> str:
    client = get_openai_client()

    invoice_details = f"""
    Vendor: {invoice.vendor_name}
    Date: {invoice.invoice_date}
    Total: {invoice.total_amount} {invoice.currency}
    Notes: {invoice.vendor_notes if invoice.vendor_notes else "None"}
    Line Items:
    {"; ".join([f"{item.description} (Qty: {item.quantity}, Price: {item.total_price})" for item in invoice.line_items])}
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Using a concrete model ID
        messages=[
            {
                "role": "system",
                "content": "You are an AI assistant that summarizes invoice details concisely.",
            },
            {
                "role": "user",
                "content": f"Please provide a brief summary of the following invoice:\n{invoice_details}",
            },
        ],
        max_tokens=150,
    )

    return response.choices[0].message.content.strip()
