from document_client import get_anthropic_client
import json
from typing import List, Dict

def document_field_extraction(text: str, field_names: List[str]) -> Dict[str, str]:
    if not text.strip() or not field_names:
        return {}
    client = get_anthropic_client()
    prompt = f"""Extract the following fields from the document text and return ONLY a valid JSON object.

Fields to extract: {', '.join(field_names)}

Document text:
{text}

Output format:
{{
  "{field_names[0]}": "extracted value or null",
  {', '.join(f'  "{f}": "value"' for f in field_names[1:])}
}}"""
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1024,
        temperature=0.1,
        messages=[{"role": "user", "content": prompt}]
    )
    try:
        extracted = json.loads(message.content[0].text.strip())
        return {k: v for k, v in extracted.items() if k in field_names}
    except json.JSONDecodeError:
        return {}