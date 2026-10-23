
import os
from openai import OpenAI
from document_models import NormalizedExpense

def get_openai_client():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")
    return OpenAI(api_key=api_key)

def summarize_invoice(expense_data: NormalizedExpense) -> str:
    """
    Generates a concise summary of an invoice using OpenAI's GPT model.

    Args:
        expense_data: A NormalizedExpense object with extracted invoice data.

    Returns:
        A string containing the summary.
    """
    if not expense_data.vendor_name:
        return "Cannot summarize: Not a valid invoice record."

    client = get_openai_client()

    prompt_content = f"""
    Summarize the following invoice in one sentence.
    Include the vendor name, the total amount, and the due date.

    Vendor: {expense_data.vendor_name}
    Total: {expense_data.currency_symbol}{expense_data.invoice_total}
    Due Date: {expense_data.due_date}
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes financial documents."},
            {"role": "user", "content": prompt_content},
        ],
        temperature=0.5,
        max_tokens=100,
    )

    summary = response.choices[0].message.content
    return summary.strip() if summary else "Failed to generate summary."
