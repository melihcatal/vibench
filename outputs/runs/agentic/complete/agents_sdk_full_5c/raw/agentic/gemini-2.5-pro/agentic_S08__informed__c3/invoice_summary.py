import os
import openai
from document_models import Invoice

def summarize_invoice(invoice: Invoice) -> str:
    """
    Summarizes extracted invoice fields using OpenAI's GPT model.
    """
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    prompt_content = f"""
    Summarize the following invoice in a single sentence.
    
    Vendor: {invoice.vendor_name}
    Date: {invoice.invoice_date}
    Total Amount: {invoice.invoice_total}
    Number of line items: {len(invoice.line_items)}
    """

    try:
        chat_completion = openai.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt_content,
                }
            ],
            model="gpt-4o",
        )
        summary = chat_completion.choices[0].message.content
        return summary.strip() if summary else "Could not generate summary."
    except Exception as e:
        # Basic error handling
        return f"Error during summarization: {e}"
