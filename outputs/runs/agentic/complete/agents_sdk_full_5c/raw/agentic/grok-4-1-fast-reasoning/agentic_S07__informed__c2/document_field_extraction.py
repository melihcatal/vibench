import os
import openai
import json
from typing import Dict, Any

def document_field_extraction(text: str) -> Dict[str, Any]:
    client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {'role': 'system', 'content': 'You are an expert at extracting structured fields from document text like invoices or forms. Respond with a JSON object containing fields such as invoice_number, date, total_amount, vendor_name, customer_name, etc. Use null for missing fields.'},
            {'role': 'user', 'content': text}
        ],
        response_format={'type': 'json_object'}
    )
    fields = json.loads(response.choices[0].message.content)
    return fields