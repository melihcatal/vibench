import os
import openai
from document_models import ExtractedInvoice


def get_invoice_summary(invoice: ExtractedInvoice) -> str:
    """
    Generates a concise summary of an invoice using OpenAI's GPT model.
    """
    if not os.environ.get("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY environment variable not set.")
        
    client = openai.OpenAI()

    prompt = f"""
    Please provide a one-sentence summary for the following invoice.
    Include the vendor name, total amount, and invoice date.

    Vendor: {invoice.vendor_name}
    Total Amount: {invoice.total_amount}
    Invoice Date: {invoice.invoice_date}
    Number of Line Items: {len(invoice.line_items)}

    Summary:
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes financial documents."},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            max_tokens=100,
        )
        summary = response.choices[0].message.content.strip()
        return summary
    except Exception as e:
        return f"Error generating summary: {e}"
