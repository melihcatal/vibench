import os
import json
from openai import OpenAI
from document_models import DocumentFields, NormalizedExpense

def normalize_expense(extracted: DocumentFields) -> NormalizedExpense:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    schema_prompt = """
{
  "document_type": "invoice" or "receipt",
  "vendor_name": "str",
  "transaction_date": "YYYY-MM-DD",
  "total_amount": "float",
  "tax_amount": "float|null",
  "line_items": [{"description": "str", "quantity": "float|null", "unit_price": "float|null", "amount": "float"}],
  "raw_confidence": "object"
}
    """
    
    prompt = f"""Normalize this extracted expense to the JSON schema above. Infer document_type from fields. Standardize date to YYYY-MM-DD. Map vendor or merchant to vendor_name. Output ONLY JSON.

Extracted data: {json.dumps(extracted.model_dump(), default=str)}

Schema example: {schema_prompt}"""
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        temperature=0.1
    )
    
    normalized_json = json.loads(response.choices[0].message.content)
    return NormalizedExpense(**normalized_json)