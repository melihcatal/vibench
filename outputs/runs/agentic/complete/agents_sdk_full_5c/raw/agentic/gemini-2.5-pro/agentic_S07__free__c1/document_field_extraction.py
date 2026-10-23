import os
import json
from typing import Dict, List
from anthropic import Anthropic

def extract_fields(text: str, fields: List[str]) -> Dict:
    """
    Extracts structured fields from text using Anthropic's Claude model.

    Args:
        text: The document text to extract information from.
        fields: A list of field names to extract.

    Returns:
        A dictionary with the extracted fields.
    """
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    prompt = f"""
From the document text provided below, extract the following fields: {', '.join(fields)}.
Return the result as a JSON object with keys corresponding to the field names.
If a field is not found, its value should be null.

Document Text:
---
{text}
---

JSON Output:
"""

    message = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    response_text = message.content[0].text
    
    try:
        # The model might return the JSON inside a code block
        json_str = response_text.strip()
        if json_str.startswith("```json"):
            json_str = json_str[7:]
        if json_str.endswith("```"):
            json_str = json_str[:-3]
        
        return json.loads(json_str.strip())
    except json.JSONDecodeError:
        return {"error": "Failed to parse JSON response from model", "response": response_text}
