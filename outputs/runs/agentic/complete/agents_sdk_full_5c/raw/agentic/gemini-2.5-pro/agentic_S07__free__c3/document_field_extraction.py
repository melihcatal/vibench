import os
import anthropic
from typing import Dict

def extract_structured_fields(document_text: str) -> Dict:
    """
    Extracts structured fields (e.g., invoice number, date) from document text
    using Anthropic's Claude model.

    Args:
        document_text: The full text extracted from a document.

    Returns:
        A dictionary of extracted fields.
    """
    # ANTHROPIC_API_KEY environment variable is read by the client
    client = anthropic.Anthropic()

    prompt = f"""
Human: From the following document text, extract the invoice number, the total amount due, and the invoice date.
Return the result as a JSON object with the keys "invoice_number", "total_amount", and "invoice_date".

Document Text:
---
{document_text}
---

Assistant:
"""

    message = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )
    
    # In a real application, you would parse the JSON from message.content
    # For this example, we return the raw text block content.
    if message.content and isinstance(message.content, list):
        return {"extracted_text": message.content[0].text}
    
    return {}
