import os
import json
from typing import Union
import openai
from document_models import Invoice, Receipt, NormalizedExpense


def normalize_expense(expense_data: Union[Invoice, Receipt]) -> NormalizedExpense:
    """
    Normalizes extracted expense data into a standard JSON schema using OpenAI.
    """
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    prompt = f"""
    Please normalize the following expense data into a standard JSON format.
    The output should be a single JSON object with the following fields:
    - vendor: The name of the vendor or merchant.
    - transaction_date: The date of the transaction.
    - total: The total amount of the expense.
    - line_items: A list of items, each with description and amount.
    - category: A suggested category for the expense (e.g., 'Office Supplies', 'Meals', 'Travel').
    - raw_text: The original text from which data was extracted.
    
    Data:
    {expense_data.model_dump_json(indent=2)}
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a data normalization assistant."},
            {"role": "user", "content": prompt},
        ],
        response_format={"type": "json_object"},
    )

    try:
        normalized_data = json.loads(response.choices[0].message.content)
        return NormalizedExpense(**normalized_data)
    except (json.JSONDecodeError, TypeError) as e:
        # Fallback to manual normalization if AI fails
        if isinstance(expense_data, Invoice):
            vendor = expense_data.vendor_name
            date = expense_data.invoice_date
        else:  # Receipt
            vendor = expense_data.merchant_name
            date = expense_data.transaction_date

        return NormalizedExpense(
            vendor=vendor,
            transaction_date=date,
            total=expense_data.total_amount,
            line_items=[item.model_dump() for item in expense_data.line_items],
        )
