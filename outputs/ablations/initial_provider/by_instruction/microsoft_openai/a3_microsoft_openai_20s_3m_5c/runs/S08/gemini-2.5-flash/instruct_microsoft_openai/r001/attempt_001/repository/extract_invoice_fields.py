from document_client import get_openai_client
from document_models import InvoiceFields, LineItem
import json

def extract_invoice_fields(document_content: str) -> InvoiceFields:
    client = get_openai_client()
    
    # Using a structured prompt for better extraction with GPT-4o
    response = client.chat.completions.create(
        model="gpt-4o", # Concrete model identifier
        response_model=InvoiceFields,
        messages=[
            {"role": "system", "content": "You are an AI assistant that extracts structured data from invoices."},
            {"role": "user", "content": f"Extract the vendor name, invoice date (in YYYY-MM-DD format), total amount, and line items (description, quantity, unit_price, total_price) from the following invoice text:\n\n{document_content}\n\nRespond with a JSON object conforming to the InvoiceFields schema."}
        ]
    )

    # The response_model argument directly returns the Pydantic model instance
    return response.choices[0].message.content
