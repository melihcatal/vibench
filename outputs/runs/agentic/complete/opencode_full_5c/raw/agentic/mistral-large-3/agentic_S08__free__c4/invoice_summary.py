from typing import Dict, Any
from document_models import NormalizedExpense
import openai


def summarize_invoice_fields(expense: NormalizedExpense) -> str:
    prompt = (
        f"Summarize the following invoice details in a concise manner:\n"
        f"Vendor: {expense.vendor}\n"
        f"Date: {expense.date}\n"
        f"Total Amount: {expense.amount} {expense.currency}\n"
        f"Tax: {expense.tax if expense.tax else 'Not specified'}\n"
        f"Line Items: {len(expense.line_items)} items\n"
        "Provide a summary in 2-3 sentences."
    )

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100,
    )

    return response.choices[0].message["content"].strip()
