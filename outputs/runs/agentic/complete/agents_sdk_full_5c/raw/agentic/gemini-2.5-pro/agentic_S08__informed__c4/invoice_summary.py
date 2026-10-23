import os
import openai
from document_models import NormalizedExpense

def summarize_invoice(expense_data: NormalizedExpense) -> str:
    """
    Generates a human-readable summary of an invoice using OpenAI's API.
    
    :param expense_data: The normalized expense data.
    :return: A string containing the summary.
    """
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    if not expense_data:
        return "No data provided to summarize."

    prompt_content = f"""
    Please provide a concise, one-paragraph summary of the following expense.
    Include the vendor, transaction date, and total amount.
    
    Vendor: {expense_data.vendor}
    Date: {expense_data.transaction_date}
    Total: {expense_data.total}
    Number of line items: {len(expense_data.line_items)}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes expense documents."},
                {"role": "user", "content": prompt_content}
            ],
            temperature=0.5,
            max_tokens=150,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating summary: {e}"

