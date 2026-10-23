import os
import json
from openai import OpenAI
from typing import Dict, Any

def validate_document_fields(extracted: Dict[str, Any]) -> Dict[str, Any]:
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    prompt = f"""Validate the following extracted document fields.

Data:
{json.dumps(extracted, default=str, indent=2)}

Validation criteria:
1. Key fields present: VENDOR_NAME or SUPPLIER_NAME (merchant), INVOICE_DATE or RECEIPT_DATE (date), INVOICE_TOTAL or TOTAL (total)
2. Confidences > 80% for key fields
3. Date format valid (YYYY-MM-DD or parseable)
4. Total > 0
5. Line items make sense (sum approx total if possible)

Output ONLY JSON:
{{
  "valid": boolean,
  "avg_confidence": float (average of all fields),
  "issues": array of strings
}}"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
        response_format={"type": "json_object"}
    )
    validation = json.loads(response.choices[0].message.content)
    return validation
