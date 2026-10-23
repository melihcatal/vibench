from typing import Dict, Any
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage


def summarize_invoice_fields(extracted_data: Dict[str, Any]) -> str:
    """
    Summarizes extracted invoice fields using Mistral Chat API.
    Model: mistral/mistral-large-latest
    """
    client = MistralClient(api_key=os.getenv("MISTRAL_API_KEY"))

    prompt = (
        "Summarize the following invoice data in a concise manner:\n"
        f"Vendor: {extracted_data.get('vendor_name', 'N/A')}\n"
        f"Date: {extracted_data.get('invoice_date', 'N/A')}\n"
        f"Total Amount: {extracted_data.get('total_amount', 'N/A')}\n"
        f"Line Items: {len(extracted_data.get('line_items', []))} items\n"
        "Provide a brief summary in 2-3 sentences."
    )

    messages = [ChatMessage(role="user", content=prompt)]
    response = client.chat(model="mistral-large-latest", messages=messages)

    return response.choices[0].message.content
