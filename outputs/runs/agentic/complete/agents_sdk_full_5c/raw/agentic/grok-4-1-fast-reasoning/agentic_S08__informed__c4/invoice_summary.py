import anthropic
import os
import json

def invoice_summary(invoice_fields: dict) -> str:
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        return "Error: Missing ANTHROPIC_API_KEY"
    client = anthropic.Anthropic(api_key=api_key)
    prompt = f"""Provide a concise human-readable summary of this invoice:

{json.dumps(invoice_fields, indent=2)}

Include key details: vendor, date, total, main items."""
    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=200,
            temperature=0.3,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text
    except Exception as e:
        return f"Error: {str(e)}"