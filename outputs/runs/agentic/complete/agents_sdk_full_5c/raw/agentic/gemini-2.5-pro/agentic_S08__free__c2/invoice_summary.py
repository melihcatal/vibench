import os
import anthropic
from typing import Dict, Any

def invoice_summary(extracted_data: Dict[str, Any]) -> str:
    """
    Summarizes extracted invoice data using Anthropic's Claude model.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set.")

    client = anthropic.Anthropic(api_key=api_key)

    prompt = f"""
    Please provide a concise, one-paragraph summary of the following invoice data.
    Focus on the vendor, the total amount, and the invoice date.

    Invoice Data:
    - Vendor: {extracted_data.get('vendor', 'N/A')}
    - Invoice Date: {extracted_data.get('date', 'N/A')}
    - Total Amount: {extracted_data.get('total', 'N/A')}
    - Number of Line Items: {len(extracted_data.get('line_items', []))}
    """

    message = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=200,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )
    
    summary = message.content[0].text if message.content else "Could not generate summary."
    return summary
