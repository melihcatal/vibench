import anthropic
import json
from typing import Dict, Any
from document_client import Config


def document_field_extraction(text: str) -> Dict[str, Any]:
    client = anthropic.Anthropic(api_key=Config.ANTHROPIC_API_KEY)
    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1000,
        messages=[
            {
                "role": "user",
                "content": f"Extract common document fields as JSON: sender_name, recipient_name, date, amount, invoice_number. Use null if missing. Output ONLY JSON.\\n\\nText:\\n{text}",
            }
        ],
    )
    content = message.content[0].text
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {{}}
