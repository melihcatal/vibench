"""
Summarize extracted invoice fields using an LLM.
"""
import os
from openai import OpenAI
from document_models import Invoice

def summarize_invoice(invoice_data: Invoice) -> str:
    """
    Generates a human-readable summary of an invoice using OpenAI's API.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    items_str = "\n".join(
        [f"- {item.description} (Qty: {item.quantity}, Total: {item.total_amount})" for item in invoice_data.items]
    )

    prompt = f"""
    Please provide a brief, one-paragraph summary of the following invoice.
    
    Vendor: {invoice_data.vendor_name}
    Date: {invoice_data.invoice_date}
    Total Amount: ${invoice_data.invoice_total}

    Line Items:
    {items_str}

    Summary:
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes financial documents."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.5,
            max_tokens=150,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating summary: {e}"
