import json
from datetime import date
from document_client import get_openai_client
from document_models import Invoice, LineItem

def extract_invoice_fields(invoice_text: str) -> Invoice:
    client = get_openai_client()

    prompt = f"""Extract the following structured data from the invoice text below:
    - Vendor Name
    - Invoice Date (YYYY-MM-DD)
    - Total Amount
    - Line Items (description, quantity, unit_price, total)

    Return the data as a JSON object matching the following Pydantic model structure:

    class LineItem(BaseModel):
        description: str
        quantity: float
        unit_price: float
        total: float

    class Invoice(BaseModel):
        vendor: str
        date: date
        total: float
        line_items: List[LineItem]

    Invoice Text:
    """{invoice_text}"""
    
    Ensure the 'date' field is in 'YYYY-MM-DD' format and valid.
    Ensure 'quantity', 'unit_price', and 'total' for line items are floats.
    The 'line_items' field should be an array, even if empty.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o", # Using a powerful model for structured extraction
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "You are an AI assistant designed to extract structured data from documents."},
                {"role": "user", "content": prompt}
            ]
        )
        
        extracted_data = json.loads(response.choices[0].message.content)
        
        # Ensure date is parsed correctly
        if 'date' in extracted_data and isinstance(extracted_data['date'], str):
            extracted_data['date'] = date.fromisoformat(extracted_data['date'])

        # Ensure line_items are parsed into LineItem models
        if 'line_items' in extracted_data and extracted_data['line_items'] is not None:
            extracted_data['line_items'] = [
                LineItem(**item) for item in extracted_data['line_items']
            ]

        return Invoice(**extracted_data)

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from OpenAI response: {e}")
        print(f"Raw response content: {response.choices[0].message.content}")
        raise
    except Exception as e:
        print(f"An error occurred during invoice extraction: {e}")
        raise
