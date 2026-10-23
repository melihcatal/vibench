from document_client import get_anthropic_client
from document_models import ExtractedInvoice

def summarize_invoice_fields(invoice: ExtractedInvoice) -> str:
    client = get_anthropic_client()

    prompt = f"""Please summarize the key details of the following invoice in a concise paragraph. 
               Include the vendor, date, total amount, and a brief mention of the line items. 
               Do not include any conversational filler.

               Invoice details:
               Vendor: {invoice.vendor}
               Date: {invoice.date}
               Total: {invoice.total}
               Line Items: {', '.join([item.description for item in invoice.line_items]) if invoice.line_items else 'N/A'}
            """

    response = client.messages.create(
        model="claude-3-opus-20240229", # Concrete model identifier
        max_tokens=200,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.content[0].text
