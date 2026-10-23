"""Normalize extracted expense fields into a standard JSON schema using OpenAI."""

import json
import os
import openai
from document_models import ExpenseNormalizationRequest, NormalizedExpenseRecord


def normalize_expense(request: ExpenseNormalizationRequest) -> NormalizedExpenseRecord:
    """Normalize extracted expense fields into a standard JSON schema using OpenAI chat completions."""
    api_key = os.environ.get("OPENAI_API_KEY", "")
    client = openai.OpenAI(api_key=api_key)

    source_data = request.to_dict()
    normalization_prompt = f"""Normalize the following extracted expense data into a standardized JSON schema.

Source data:
{json.dumps(source_data, indent=2, default=str)}

Output ONLY a valid JSON object matching this schema:
{{
  "expense_type": "string (one of: invoice, receipt, purchase_order)",
  "vendor_name": "string",
  "document_date": "string (ISO 8601 date format YYYY-MM-DD)",
  "currency": "string (ISO 4217 code, default USD if unknown)",
  "subtotal": "number or null",
  "tax_amount": "number or null",
  "total_amount": "number",
  "line_items": [
    {{
      "description": "string",
      "quantity": "number or null",
      "unit_price": "number or null",
      "total_price": "number or null"
    }}
  ],
  "document_id": "string or null",
  "confidence": "number (0-1)",
  "source_provider": "string"
}}

If any field cannot be determined, use null. Parse numeric values from strings if needed."""

    response = client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        messages=[
            {
                "role": "system",
                "content": "You are an expense data normalization assistant. Output only valid JSON matching the requested schema.",
            },
            {"role": "user", "content": normalization_prompt},
        ],
        temperature=0.0,
        max_tokens=2048,
    )

    content = response.choices[0].message.content.strip()
    if content.startswith("```json"):
        content = content.split("```json", 1)[1].split("```", 1)[0].strip()
    elif content.startswith("```"):
        content = content.split("```", 1)[1].split("```", 1)[0].strip()

    normalized = json.loads(content)

    return NormalizedExpenseRecord(
        expense_type=normalized.get("expense_type", "unknown"),
        vendor_name=normalized.get("vendor_name", ""),
        document_date=normalized.get("document_date"),
        currency=normalized.get("currency", "USD"),
        subtotal=normalized.get("subtotal"),
        tax_amount=normalized.get("tax_amount"),
        total_amount=normalized.get("total_amount"),
        line_items=normalized.get("line_items", []),
        document_id=normalized.get("document_id"),
        confidence=normalized.get("confidence", 0.0),
        source_provider=normalized.get("source_provider", "openai_normalized"),
    )


if __name__ == "__main__":
    from document_models import InvoiceExtractionResponse
    sample = InvoiceExtractionResponse(
        vendor="Acme Corp",
        invoice_date="2024-01-15",
        total_amount="$1,250.00",
        invoice_id="INV-2024-001",
        line_items=[],
        confidence=0.95,
        provider="aws_textract",
    )
    req = ExpenseNormalizationRequest.from_invoice(sample)
    result = normalize_expense(req)
    print(result)
