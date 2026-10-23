import os
import json
from anthropic import Anthropic
from document_models import FieldsResponse

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def document_field_extraction(text: str) -> FieldsResponse:
    prompt = f"""Extract the following fields as JSON from the document text: name, date, amount.

Document text:
{text}

Respond only with valid JSON:
{{"name": "", "date": "", "amount": ""}}"""
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    fields = json.loads(message.content[0].text)
    return {"fields": fields}
