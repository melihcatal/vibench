import os
import json
from openai import OpenAI
from document_models import NormalizedExpense


def normalize_expense(
    extraction: dict, document_type: str, source_document_id: str
) -> NormalizedExpense:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""))

    system_prompt = """You are an expense data normalization assistant. Convert the provided extraction into a standardized JSON expense record.
Return ONLY valid JSON matching this schema:
{
  "vendor": string,
  "date": string (YYYY-MM-DD),
  "total": number,
  "tax": number,
  "currency": string (ISO 4217),
  "line_items": [{"description": string, "quantity": number, "unit_price": number, "amount": number}],
  "confidence": number (0.0 to 1.0)
}"""

    user_prompt = f"Normalize this {document_type} extraction into standard format:\n{json.dumps(extraction, default=str)}"

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type": "json_object"},
        temperature=0.0,
    )

    result = json.loads(response.choices[0].message.content)

    return NormalizedExpense(
        document_type=document_type,
        vendor=result.get("vendor", ""),
        date=result.get("date", ""),
        total=float(result.get("total", 0.0)),
        tax=float(result.get("tax", 0.0)),
        currency=result.get("currency", "USD"),
        line_items=result.get("line_items", []),
        source_document_id=source_document_id,
        confidence=float(result.get("confidence", 0.0)),
        metadata={"normalization_model": "gpt-4o", "provider": "openai"},
    )
