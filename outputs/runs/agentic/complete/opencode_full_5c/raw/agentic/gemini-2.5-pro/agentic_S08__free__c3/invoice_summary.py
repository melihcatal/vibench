import os
import openai
from document_models import Invoice


def invoice_summary(invoice: Invoice) -> str:
    """
    Summarizes extracted invoice fields using OpenAI's GPT-4.
    """
    if not isinstance(invoice, Invoice):
        raise TypeError("Input must be an Invoice object.")

    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    prompt = f"""
    Summarize the following invoice in a single paragraph:
    - Vendor: {invoice.vendor_name}
    - Date: {invoice.invoice_date}
    - Total: ${invoice.total_amount:.2f}
    - Line Items:
    """
    for item in invoice.line_items:
        prompt += f"  - {item.description}: ${item.amount:.2f}\n"

    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that summarizes invoices.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=150,
        )
        summary = response.choices[0].message.content
        return summary.strip() if summary else "Could not generate summary."
    except Exception as e:
        # In a real app, log the error
        return f"Error generating summary: {e}"
