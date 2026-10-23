from document_client import get_openai_client
from document_models import ExtractedInvoice, ExtractedReceipt, NormalizedExpense, LineItem
import json
from datetime import date
from typing import Union, Dict, Any

def normalize_expense(extracted_data: Union[ExtractedInvoice, ExtractedReceipt]) -> NormalizedExpense:
    client = get_openai_client()

    if isinstance(extracted_data, ExtractedInvoice):
        document_type = "invoice"
        vendor_name = extracted_data.vendor
        transaction_date = extracted_data.date
        total_amount = extracted_data.total
        line_items_data = [
            {
                "description": item.description,
                "quantity": item.quantity,
                "unit_price": item.unit_price,
                "total": item.total
            }
            for item in extracted_data.line_items
        ]
        original_data = extracted_data.model_dump() # Use model_dump for Pydantic v2
    elif isinstance(extracted_data, ExtractedReceipt):
        document_type = "receipt"
        vendor_name = extracted_data.merchant
        # Receipts often lack explicit dates, use today's date or infer if possible
        transaction_date = date.today() 
        total_amount = extracted_data.total
        # Receipts items might be simpler, map to LineItem if possible or leave raw
        line_items_data = [] 
        for item in extracted_data.items:
            # Attempt to map receipt items to LineItem schema, can be refined based on actual receipt item structure
            line_items_data.append({
                "description": item.get("description", ""),
                "quantity": item.get("quantity", 1.0),
                "unit_price": item.get("price", 0.0),
                "total": item.get("price", 0.0) # Assuming price is total for single item
            })
        original_data = extracted_data.model_dump()
    else:
        raise ValueError("Unsupported extracted data type")

    # Construct a preliminary normalized expense object
    preliminary_normalized_expense = {
        "document_type": document_type,
        "vendor_name": vendor_name,
        "transaction_date": transaction_date.isoformat(),
        "total_amount": total_amount,
        "line_items": line_items_data,
        "original_data": original_data,
    }

    prompt = f"""Normalize the following extracted document data into a standard JSON schema. 
               Ensure strict adherence to the NormalizedExpense Pydantic model structure. 
               The `transaction_date` should be in YYYY-MM-DD format. 
               If any field is missing or inconsistent, infer a reasonable value or use a default. 
               Return the normalized data as a JSON object.
               
               Pydantic Model for NormalizedExpense:
               {{
                   "document_type": "string",
                   "vendor_name": "string",
                   "transaction_date": "YYYY-MM-DD string",
                   "total_amount": "float",
                   "currency": "string",
                   "line_items": [
                       {{
                           "description": "string",
                           "quantity": "float",
                           "unit_price": "float",
                           "total": "float"
                       }}
                   ],
                   "notes": "string | null",
                   "original_data": {{ "any" : "any" }},
                   "validation_status": "string",
                   "confidence_score": "float | null"
               }}
               
               Extracted data to normalize:
               {json.dumps(preliminary_normalized_expense, indent=2)}
            """

    response = client.chat.completions.create(
        model="gpt-4o", # Concrete model identifier for normalization assistance
        messages=[
            {"role": "user", "content": prompt}
        ],
        response_format={ "type": "json_object" },
        temperature=0.0
    )

    normalized_data = json.loads(response.choices[0].message.content)
    
    # Ensure date is a date object
    if 'transaction_date' in normalized_data and isinstance(normalized_data['transaction_date'], str):
        normalized_data['transaction_date'] = date.fromisoformat(normalized_data['transaction_date'])
    
    # Ensure line items are LineItem objects
    normalized_line_items = []
    if 'line_items' in normalized_data and isinstance(normalized_data['line_items'], list):
        for item_data in normalized_data['line_items']:
            normalized_line_items.append(LineItem(**item_data))
    normalized_data['line_items'] = normalized_line_items

    return NormalizedExpense(**normalized_data)
