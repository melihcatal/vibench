from anthropic import Anthropic
import os
import json
import re
from typing import Dict, Any

def document_field_extraction(text: str) -> Dict[str, Any]:
    """Extract structured fields from OCR-normalized document text."""
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1024,
        temperature=0,
        system="Extract all possible structured fields (name, address, date, amount, email, etc.) from the document text. Respond ONLY with a valid JSON object, no other text.",
        messages=[{"role": "user", "content": text}]
    )
    content = message.content[0].text
    
    json_str = re.search(r'\{.*\}', content, re.DOTALL)
    if json_str:
        try:
            return json.loads(json_str.group())
        except json.JSONDecodeError:
            pass
    return {}
