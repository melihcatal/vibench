import os
import json
from typing import Dict, Any
from anthropic import Anthropic


def document_field_extraction(text: str) -> Dict[str, Any]:
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    prompt = f"""Analyze the following document text and extract all identifiable structured fields into a JSON object.

Document:
{text}

Fields to extract: name, address, date, amount, email, phone, organization, invoice_number, etc. Use null for missing values.

Respond ONLY with valid JSON object, no other text."""
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1024,
        temperature=0,
        messages=[{"role": "user", "content": prompt}],
    )
    content_text = message.content[0].text.strip()
    return json.loads(content_text)
