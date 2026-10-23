import os
import openai
from document_models import Invoice


def summarize_invoice(invoice: Invoice) -> str:
    """
    Generates a human-readable summary of an invoice using OpenAI's GPT model.
    """
    if not isinstance(invoice, Invoice):
        raise TypeError("Input must be an Invoice object.")

    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    line_items_summary = "\n".join(
        [
            f"- {item.description or 'N/A'}: {item.quantity or 'N/A'} x ${item.unit_price or 0.0:.2f} = ${item.total_price or 0.0:.2f}"
            for item in invoice.line_items
        ]
    )

    prompt = f"""
    Summarize the following invoice in a single paragraph:

    - Vendor: {invoice.vendor_name or "N/A"}
    - Customer: {invoice.customer_name or "N/A"}
    - Invoice Date: {invoice.invoice_date or "N/A"}
    - Due Date: {invoice.due_date or "N/A"}
    - Total Amount: ${invoice.total_amount or 0.0:.2f}
    - Items:
    {line_items_summary}
    """

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that summarizes financial documents.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.5,
            max_tokens=150,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating summary: {e}"
