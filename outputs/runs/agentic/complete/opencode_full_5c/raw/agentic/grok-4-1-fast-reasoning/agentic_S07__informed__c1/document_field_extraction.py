import os
import json
from typing import Dict, Any
from openai import OpenAI


def document_field_extraction(text: str) -> Dict[str, Any]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not set")
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Extract the following fields from the document text as a JSON object: invoice_number (str or null), date (str or null), total_amount (float or null), vendor_name (str or null), customer_name (str or null), address (str or null). Return only valid JSON.",
            },
            {"role": "user", "content": text},
        ],
        response_format={"type": "json_object"},
        temperature=0.1,
    )
    fields = json.loads(response.choices[0].message.content)
    return fields
