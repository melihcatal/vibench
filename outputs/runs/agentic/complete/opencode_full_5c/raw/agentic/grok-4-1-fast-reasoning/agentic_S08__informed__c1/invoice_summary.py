import os
import json
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from document_models import InvoiceFields


def generate_invoice_summary(invoice: InvoiceFields) -> str:
    client = MistralClient(api_key=os.getenv("MISTRAL_API_KEY"))
    messages = [
        ChatMessage(
            role="user",
            content=f"Summarize this invoice concisely:\n{json.dumps(invoice.model_dump(), default=str)}",
        )
    ]
    response = client.chat(model="mistral-large-latest", messages=messages)
    return response.choices[0].message.content
