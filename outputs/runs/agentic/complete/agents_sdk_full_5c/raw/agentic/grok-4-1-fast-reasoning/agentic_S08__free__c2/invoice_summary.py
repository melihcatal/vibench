import os
import anthropic
from typing import Dict, Any

def generate_invoice_summary(extracted_invoice: Dict[str, Any]) -> str:
    client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=500,
        messages=[
            {
                "role": "user",
                "content": f"Provide a concise summary of this invoice extraction:\n{extracted_invoice}"
            }
        ]
    )
    return message.content[0].text
