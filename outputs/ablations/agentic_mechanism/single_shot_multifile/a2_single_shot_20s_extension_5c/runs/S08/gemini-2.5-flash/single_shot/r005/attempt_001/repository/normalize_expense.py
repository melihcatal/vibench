import json
import uuid
from typing import Dict, Any, Optional
from document_client import get_openai_client
from document_models import NormalizedExpense, LineItem

NORMALIZED_EXPENSE_SCHEMA = """
{
  "type": "object",
  "properties": {
    "id": { "type": "string", "description": "Unique ID for the expense record" },
    "document_type": { "type": "string", "enum": ["invoice", "receipt"] },
    "vendor_name": { "type": "string", "description": "Name of the vendor or merchant" },
    "transaction_date": { "type": "string", "format": "date", "description": "Date of the transaction in YYYY-MM-DD format" },
    "total_amount": { "type": "number", "description": "Total amount of the expense" },
    "currency": { "type": "string", "description": "Currency of the transaction, e.g., USD, EUR" },
    "tax_amount": { "type": "number", "nullable": true, "description": "Total tax amount, if available" },
    "line_items": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "description": { "type": "string" },
          "quantity": { "type": "number", "nullable": true },
          "unit_price": { "type": "number", "nullable": true },
          "amount": { "type": "number" }
        },
        "required": ["description", "amount"]
      }
    },
    "notes": { "type": "string", "nullable": true, "description": "Any additional notes or memo text" }
  },
  "required": ["id", "document_type", "vendor_name", "transaction_date", "total_amount", "currency", "line_items"]
}
"""

def normalize_expense_fields(
    extracted_data: Dict[str, Any],
    document_type: str,
    original_notes: Optional[str] = None
) -> NormalizedExpense:
    """
    Normalizes extracted expense fields into a standard JSON schema using OpenAI GPT.
    The LLM will infer missing fields or correct formats where possible.
    """
    openai_client = get_openai_client()

    input_data_str = json.dumps(extracted_data, indent=2)

    prompt_messages = [
        {"role": "system", "content": f"You are an expert at normalizing structured expense data into a strict JSON schema. The currency should be inferred from common context, default to USD if ambiguous. Ensure the transaction_date is in YYYY-MM-DD format. Generate a unique 'id' for the record."}, 
        {"role": "user", "content": f"Normalize the following extracted {document_type} data into the provided JSON schema.\n\nExtracted Data:\n{input_data_str}\n\nTarget Schema:\n{NORMALIZED_EXPENSE_SCHEMA}\n\nEnsure your response is ONLY the normalized JSON object, nothing else. If 'notes' is provided, include it as is. Original notes: {original_notes if original_notes else 'None'}"}
    ]

    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=prompt_messages,
            response_format={"type": "json_object"}
        )
        normalized_json_str = response.choices[0].message.content
        normalized_data = json.loads(normalized_json_str)

        if 'id' not in normalized_data or not normalized_data['id']:
            normalized_data['id'] = str(uuid.uuid4())
        
        normalized_data['document_type'] = document_type
        if 'currency' not in normalized_data or not normalized_data['currency']:
            normalized_data['currency'] = 'USD'
        
        if original_notes and 'notes' not in normalized_data:
            normalized_data['notes'] = original_notes
        
        normalized_data['extracted_source'] = extracted_data

        return NormalizedExpense(**normalized_data)
    except Exception as e:
        print(f"Error during normalization with OpenAI: {e}")
        fallback_data = {
            'id': str(uuid.uuid4()),
            'document_type': document_type,
            'vendor_name': extracted_data.get('vendor_name', extracted_data.get('merchant_name', 'Unknown Vendor')),
            'transaction_date': extracted_data.get('invoice_date', extracted_data.get('transaction_date', '2000-01-01')),
            'total_amount': extracted_data.get('invoice_total', extracted_data.get('total_amount', 0.0)),
            'currency': 'USD',
            'tax_amount': extracted_data.get('tax_amount'),
            'line_items': extracted_data.get('line_items', extracted_data.get('items', [])),
            'notes': original_notes,
            'extracted_source': extracted_data
        }
        return NormalizedExpense(**fallback_data)
