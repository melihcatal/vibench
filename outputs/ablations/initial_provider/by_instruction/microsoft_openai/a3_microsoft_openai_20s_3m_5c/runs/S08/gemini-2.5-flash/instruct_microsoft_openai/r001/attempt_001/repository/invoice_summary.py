from document_models import InvoiceFields
from document_client import get_openai_client # Concrete provider: OpenAI

def summarize_invoice(invoice_fields: InvoiceFields) -> str:
    client = get_openai_client()

    # Construct a detailed prompt for summarization
    summary_prompt = f"""
    Summarize the following invoice details in a concise paragraph. Highlight the vendor, total amount, and key line items.

    Vendor: {invoice_fields.vendor_name}
    Date: {invoice_fields.invoice_date}
    Total Amount: {invoice_fields.total_amount}

    Line Items:
    """
    for item in invoice_fields.line_items:
        summary_prompt += f"- {item.description} (Qty: {item.quantity}, Unit Price: {item.unit_price}, Total: {item.total_price})\n"

    response = client.chat.completions.create(
        model="gpt-3.5-turbo", # Concrete model identifier
        messages=[
            {"role": "system", "content": "You are an AI assistant that summarizes invoice information."},
            {"role": "user", "content": summary_prompt}
        ],
        max_tokens=200
    )

    return response.choices[0].message.content.strip()
