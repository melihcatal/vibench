import os
from typing import Dict, Any
from openai import OpenAI
from document_models import NormalizedExpense


def summarize_invoice(expense: NormalizedExpense) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    prompt = f"""Summarize the following expense in a concise paragraph:
    Vendor/Merchant: {expense.vendor_merchant}
    Date: {expense.date}
    Total: {expense.total_amount}
    Tax: {expense.tax_amount}
    Items: {', '.join([item['description'] for item in expense.items])}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()