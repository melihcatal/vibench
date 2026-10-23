# document_field_extraction.py
import os
import json
from anthropic import Anthropic
from document_models import ExtractedFields

def extract_fields_from_text(text: str, desired_fields: str) -> ExtractedFields:
    """
    Extracts structured fields from text using Anthropic's Claude model.
    
    Requires ANTHROPIC_API_KEY environment variable.
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set.")
        
    client = Anthropic(api_key=api_key)

    prompt = f"""
From the following document text, extract the specified fields and return them as a valid JSON object.
The desired fields are: {desired_fields}.
If a field is not found, its value should be null.

Document Text:
---
{text}
---

JSON Output:
"""

    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    response_text = message.content[0].text
    
    try:
        # Claude is good at returning just the JSON, but sometimes it might be in a code block
        json_str = response_text.strip().lstrip("```json").rstrip("```").strip()
        data = json.loads(json_str)
        return ExtractedFields(data=data)
    except json.JSONDecodeError:
        # Handle cases where the output is not valid JSON
        return ExtractedFields(data={"error": "Failed to parse LLM response as JSON", "raw_response": response_text})
