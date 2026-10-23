import os
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from document_models import NormalizedExpense

def invoice_summary(normalized: NormalizedExpense) -> str:
    client = MistralClient(api_key=os.getenv("MISTRAL_API_KEY"))
    
    messages = [
        ChatMessage(
            role="user",
            content=f"Provide a concise 2-3 sentence summary of this expense invoice, highlighting key details like vendor, date, total, and major line items: {normalized.model_dump_json()}"
        )
    ]
    
    response = client.chat(
        model="mistral-large-latest",
        messages=messages
    )
    
    return response.choices[0].message.content