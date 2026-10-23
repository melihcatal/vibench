from document_client import get_openai_client
from document_models import ExtractedInvoice, LineItem
import json
from datetime import date

def extract_invoice_fields(invoice_image_base64: str) -> ExtractedInvoice:
    client = get_openai_client()
    
    prompt = """You are an expert at extracting structured data from invoices. 
               Extract the vendor name, invoice date (YYYY-MM-DD), total amount, and line items (description, quantity, unit_price, total) from the provided invoice image. 
               Return the data as a JSON object strictly conforming to the following Pydantic model:
               {
                   "vendor": "string",
                   "date": "YYYY-MM-DD string",
                   "total": "float",
                   "line_items": [
                       {
                           "description": "string",
                           "quantity": "float",
                           "unit_price": "float",
                           "total": "float"
                       }
                   ]
               }
               If a field is not found, use a reasonable default or omit it if optional.
               The invoice image is provided in base64 format.
            """

    response = client.chat.completions.create(
        model="gpt-4o", # Concrete model identifier
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{invoice_image_base64}"}
                    }
                ]
            }
        ],
        response_format={ "type": "json_object" },
        temperature=0.0
    )
    
    extracted_data = json.loads(response.choices[0].message.content)
    
    # Convert date string to date object
    if 'date' in extracted_data and isinstance(extracted_data['date'], str):
        extracted_data['date'] = date.fromisoformat(extracted_data['date'])

    # Convert line items to LineItem objects if present
    line_items = []
    if 'line_items' in extracted_data and isinstance(extracted_data['line_items'], list):
        for item_data in extracted_data['line_items']:
            line_items.append(LineItem(**item_data))
    extracted_data['line_items'] = line_items

    return ExtractedInvoice(**extracted_data)
