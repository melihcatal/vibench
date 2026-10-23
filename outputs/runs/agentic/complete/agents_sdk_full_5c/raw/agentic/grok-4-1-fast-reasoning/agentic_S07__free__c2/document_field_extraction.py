from anthropic import Anthropic
import os
import json

def document_field_extraction(text: str, field_names: list[str]) -> dict:
    client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
    prompt = f"""Extract the following fields from the document as a JSON object with keys matching the field names.
Fields: {', '.join(field_names)}
Document text:
{text}
Respond ONLY with valid JSON."""
    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    content = message.content[0].text
    return json.loads(content)
