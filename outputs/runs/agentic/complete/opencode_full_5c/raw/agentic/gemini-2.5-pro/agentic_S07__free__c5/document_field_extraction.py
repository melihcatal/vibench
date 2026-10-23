import anthropic
from document_client import get_anthropic_client
from document_models import ExtractedFields


def extract_fields_from_text(text: str, desired_fields: list[str]) -> ExtractedFields:
    anthropic_client = get_anthropic_client()

    fields_prompt = ", ".join(desired_fields)

    prompt = f"""
Human: From the following document text, extract the following fields: {fields_prompt}.
Return the result as a JSON object. If a field is not found, its value should be null.

Document text:
---
{text}
---

Assistant:
"""

    message = anthropic_client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    # The response is expected to be a JSON string.
    import json

    extracted_json = json.loads(message.content[0].text)

    return ExtractedFields(fields=extracted_json)
