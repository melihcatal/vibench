import os
from typing import Dict, Any
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from document_models import NormalizedExpense


def summarize_invoice(expense: NormalizedExpense) -> str:
    """
    Summarizes extracted invoice fields using Mistral Chat API.
    """
    api_key = os.getenv("MISTRAL_API_KEY")
    model = "mistral-tiny"

    client = MistralClient(api_key=api_key)

    prompt = f"""
    Summarize the following expense in a concise paragraph:
    
    Vendor/Merchant: {expense.vendor_or_merchant}
    Date: {expense.date}
    Total Amount: {expense.total_amount}
    Tax Amount: {expense.tax_amount}
    
    Line Items:
    {chr(10).join([f"- {item.description}: {item.amount}" for item in expense.line_items])}
    """

    messages = [ChatMessage(role="user", content=prompt)]
    response = client.chat(model=model, messages=messages)

    return response.choices[0].message.content