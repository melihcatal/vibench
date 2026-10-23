import os
import json
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage


def generate_invoice_summary(expense_record: dict) -> str:
    """
    Generate a natural language summary of the normalized invoice using Mistral AI.
    """
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError("MISTRAL_API_KEY required.")

    client = MistralClient(api_key=api_key)
    messages = [
        ChatMessage(
            role="user",
            content=f"""Summarize this expense record in 3 bullet points:
- Vendor/merchant, date, total
- Key line items
- Any tax or notes

Record: {json.dumps(expense_record, indent=2)}""",
        )
    ]

    chat_response = client.chat(
        model="mistral-large-latest", messages=messages, max_tokens=200
    )

    return chat_response.choices[0].message.content.strip()
