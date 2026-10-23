from typing import Dict, Any
from document_models import NormalizedExpense
from openai import OpenAI
import os


def summarize_invoice_fields(expense: NormalizedExpense) -> str:
    """Summarize extracted invoice fields using OpenAI's GPT-4 model."""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "your-openai-api-key"))

    prompt = (
        f"Summarize the following invoice details in a concise manner:\n"
        f"Vendor: {expense.vendor}\n"
        f"Date: {expense.date}\n"
        f"Total: {expense.total} {expense.currency if expense.currency else ''}\n"
        f"Tax: {expense.tax if expense.tax else 'Not specified'}\n"
        f"Items:\n"
    )

    for item in expense.items:
        prompt += f"- {item.description}: {item.quantity} x {item.unit_price} = {item.amount}\n"

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes invoices.",
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=150,
    )

    return response.choices[0].message.content.strip()
