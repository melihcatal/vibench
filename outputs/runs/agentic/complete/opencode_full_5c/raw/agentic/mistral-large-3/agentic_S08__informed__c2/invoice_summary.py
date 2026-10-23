from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import os
from typing import Dict, Any, List

# Provider-specific: Mistral Chat API
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
client = MistralClient(api_key=MISTRAL_API_KEY)


def summarize_invoice_fields(extracted_data: Dict[str, Any]) -> str:
    """
    Summarize extracted invoice fields using Mistral's hosted LLM.
    """
    vendor = extracted_data.get("vendor", extracted_data.get("merchant", "Unknown"))
    date = extracted_data.get("date", "Unknown")
    total = extracted_data.get("total_amount", extracted_data.get("total", 0.0))
    line_items = extracted_data.get("line_items", [])

    line_items_summary = "\n".join(
        [
            f"- {item['description']}: ${item['amount']:.2f} x {item['quantity']}"
            for item in line_items
        ]
    )

    prompt = f"""
    Summarize the following invoice details in a concise and professional manner:
    
    Vendor: {vendor}
    Date: {date}
    Total Amount: ${total:.2f}
    
    Line Items:
    {line_items_summary}
    
    Summary:
    """

    messages = [ChatMessage(role="user", content=prompt)]

    response = client.chat(model="mistral-large-latest", messages=messages)

    return response.choices[0].message.content
