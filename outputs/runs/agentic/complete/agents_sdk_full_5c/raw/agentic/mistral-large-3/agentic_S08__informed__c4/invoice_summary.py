from typing import Dict, Any
import os
from openai import OpenAI
from document_models import NormalizedExpense


def summarize_invoice_fields(expense: NormalizedExpense) -> str:
    """
    Summarizes extracted invoice fields using OpenAI's GPT-4 model.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = (
        f"Summarize the following expense in a concise manner:\n"
        f"Vendor/Merchant: {expense.vendor_merchant}\n"
        f"Date: {expense.transaction_date}\n"
        f"Total Amount: {expense.total_amount}\n"
        f"Tax Amount: {expense.tax_amount}\n"
        f"Items:\n"
    )
    for item in expense.items:
        prompt += f"- {item.description}: {item.amount}\n"

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150
    )
    return response.choices[0].message.content.strip()