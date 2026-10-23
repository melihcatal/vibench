import os
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from document_models import NormalizedExpense
from typing import Dict, Any

def invoice_summary(normalized: NormalizedExpense) -> str:
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError("Set MISTRAL_API_KEY")

    client = MistralClient(api_key=api_key)

    messages = [ChatMessage(role="user", content=f"Summarize this invoice in one paragraph:\n{normalized}")]

    response = client.chat(model="mistral-large-latest", messages=messages)

    return response.choices[0].message.content