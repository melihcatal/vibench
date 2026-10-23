import os
import openai
from document_models import Invoice


def summarize_invoice(invoice: Invoice) -> str:
    """Summarizes invoice details using OpenAI's GPT model."""
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    prompt = f"""
    Summarize the following invoice in a single paragraph:
    
    Vendor: {invoice.vendor_name}
    Invoice ID: {invoice.invoice_id}
    Date: {invoice.invoice_date}
    Total Amount: {invoice.total} {invoice.currency}
    
    Line Items:
    """
    for item in invoice.line_items:
        prompt += f"- {item.description}: {item.amount}\n"

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that summarizes invoices.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=150,
            temperature=0.5,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating summary: {e}"
