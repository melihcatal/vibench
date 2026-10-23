from typing import Dict, Any
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from document_client import get_mistral_client


def summarize_invoice(invoice_data: Dict[str, Any]) -> str:
    client = get_mistral_client()

    prompt = f"""
    Summarize the following invoice data concisely. Focus on the vendor, date, total amount, and number of line items.

    Invoice Data:
    {invoice_data}
    """

    messages = [ChatMessage(role="user", content=prompt)]

    chat_response = client.chat(
        model="mistral-tiny",
        messages=messages,
    )

    summary = chat_response.choices[0].message.content
    return summary
