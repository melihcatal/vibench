import os
from openai import OpenAI
from document_models import Invoice


def summarize_invoice(invoice: Invoice) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    prompt = f"""
    Summarize the following invoice:
    - Vendor: {invoice.vendor_name}
    - Date: {invoice.invoice_date}
    - Total: {invoice.invoice_total}
    - Line Items:
    """
    for item in invoice.line_items:
        prompt += f"  - {item.description}: {item.total_price}\n"

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes invoices.",
            },
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content
