import os
import openai
from document_models import Invoice

def summarize_invoice(invoice: Invoice) -> str:
    """
    Generates a concise summary of an invoice using OpenAI's GPT models.
    """
    if not invoice:
        return "No invoice data provided."

    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    prompt_content = f"""
    Please provide a short, one-sentence summary of the following invoice:
    - Vendor: {invoice.vendor_name}
    - Date: {invoice.invoice_date}
    - Total Amount: {invoice.invoice_total}
    - Number of line items: {len(invoice.line_items)}
    
    Example: Invoice from {invoice.vendor_name} for ${invoice.invoice_total} on {invoice.invoice_date}.
    """

    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert at summarizing financial documents.",
                },
                {"role": "user", "content": prompt_content},
            ],
            max_tokens=50,
            temperature=0.2,
        )
        summary = completion.choices[0].message.content
        return summary.strip() if summary else "Could not generate summary."
    except Exception as e:
        # In a real app, you'd want more robust error handling/logging
        print(f"Error calling OpenAI API: {e}")
        return "Error generating summary."
