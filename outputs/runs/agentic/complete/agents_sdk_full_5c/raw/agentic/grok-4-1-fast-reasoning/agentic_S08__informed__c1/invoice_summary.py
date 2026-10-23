import os
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from document_models import ExtractedInvoice

def summarize_invoice(extracted: ExtractedInvoice) -> str:
    client = MistralClient(api_key=os.getenv('MISTRAL_API_KEY'))
    messages = [
        ChatMessage(role="system", content="You are a helpful assistant that summarizes invoices concisely."),
        ChatMessage(
            role="user",
            content=f"Summarize this invoice: Vendor: {extracted['vendor']}, Date: {extracted['date']}, Total: ${extracted['total']:.2f}, {len(extracted['line_items'])} line items."
        )
    ]
    response = client.chat(
        model="mistral-large-latest",
        messages=messages
    )
    return response.choices[0].message.content
