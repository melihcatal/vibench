import os
import json
from openai import OpenAI
from document_models import ExpenseRecord


def normalize_expense(raw_extraction: dict) -> dict:
    """
    Normalize raw extraction from invoice or receipt to standard ExpenseRecord schema using OpenAI.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY required.")

    client = OpenAI(api_key=api_key)

    doc_type = "invoice" if "vendor" in raw_extraction else "receipt"
    if "items" in raw_extraction:
        raw_extraction["line_items"] = raw_extraction.pop("items")
    if "merchant" in raw_extraction:
        raw_extraction["vendor"] = raw_extraction.pop("merchant")

    schema = json.dumps(ExpenseRecord.model_json_schema())

    prompt = f"""Normalize this {doc_type} extraction to the following JSON schema exactly.

Raw: {json.dumps(raw_extraction, indent=2)}

SCHEMA: {schema}

Rules:
- doc_type: "{doc_type}"
- vendor_or_merchant: use vendor or merchant value
- date: YYYY-MM-DD format
- total, amounts: float
- tax: float if present
- line_items: array with description, quantity?, unit_price?, amount

Output ONLY the JSON object."""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Output only valid JSON matching the schema.",
            },
            {"role": "user", "content": prompt},
        ],
        response_format={"type": "json_object"},
        temperature=0.0,
    )

    normalized = json.loads(response.choices[0].message.content)
    ExpenseRecord.model_validate(normalized)  # validate
    return normalized
