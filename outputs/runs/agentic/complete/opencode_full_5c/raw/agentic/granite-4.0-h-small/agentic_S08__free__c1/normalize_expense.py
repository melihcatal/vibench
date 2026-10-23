# [SAME-SCENARIO] normalize_expense.py

# Normalizes extracted expense fields to a common JSON schema using OpenAI JSON mode
import json
from openai import OpenAI
from document_client import DocumentClient


def normalize_expense(extracted_fields):
    """Normalize extracted fields to a standard expense JSON schema.

    Uses OpenAI's JSON generation to enforce schema consistency.
    Required schema:
    {
        "vendor": str,
        "date": str,
        "total": float,
        "items": list[str]
    }
    """
    prompt = f'Normalize the following structured data into valid JSON matching this schema:\n{{"vendor": str, "date": str, "total": number, "items": array of strings}}\n\nData:\n{json.dumps(extracted_fields, indent=2)}'
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        response_format={"type": "json_object"},
    )
    return response.choices[0].message.parsed
