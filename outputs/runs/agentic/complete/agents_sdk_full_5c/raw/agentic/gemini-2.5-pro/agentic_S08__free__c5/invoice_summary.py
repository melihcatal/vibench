# invoice_summary.py
from document_client import get_openai_client
from document_models import NormalizedExpense

def summarize_invoice_with_openai(expense: NormalizedExpense) -> str:
    """
    Generates a human-readable summary of an invoice using OpenAI.
    """
    client = get_openai_client()

    prompt = f"""
        Based on the following structured expense data, generate a concise, one-paragraph summary
        for an expense report. Mention the vendor, total amount, and the date.

        Data:
        - Vendor: {expense.vendor}
        - Date: {expense.transaction_date}
        - Total: {expense.total} {expense.currency}
        - Number of line items: {len(expense.line_items)}
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes expenses."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.5,
        max_tokens=150,
    )
    
    return response.choices[0].message.content.strip()
