import os
from google.cloud import documentai_v1 as documentai
from google.api_core.client_options import ClientOptions
from document_models import Receipt, Item

def extract_receipt_fields(receipt_content: bytes, project_id: str, location: str, processor_id: str) -> Receipt:
    # Define the client options with the region
    client_options = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    client = documentai.DocumentProcessorServiceClient(client_options=client_options)

    # The full resource name of the processor
    name = client.processor_path(project_id, location, processor_id)

    # Read the file into memory
    document = documentai.RawDocument(
        content=receipt_content,
        mime_type="application/pdf" # Assuming PDF for receipts, adjust if other types are expected
    )

    # Configure the process request
    request = documentai.ProcessRequest(
        name=name,
        raw_document=document
    )

    # Process the document
    result = client.process_document(request=request)
    document = result.document

    merchant_name = ""
    total_amount = 0.0
    tax_amount = 0.0
    items = []

    # Extract fields from entities
    for entity in document.entities:
        if entity.type == "merchant_name":
            merchant_name = entity.mention_text
        elif entity.type == "total_amount":
            try:
                total_amount = float(entity.mention_text)
            except ValueError:
                pass # Handle cases where conversion fails
        elif entity.type == "tax_amount":
            try:
                tax_amount = float(entity.mention_text)
            except ValueError:
                pass # Handle cases where conversion fails
        elif entity.type == "line_item":
            item_description = ""
            item_quantity = 0.0
            item_price = 0.0
            for prop in entity.properties:
                if prop.type == "description":
                    item_description = prop.mention_text
                elif prop.type == "quantity":
                    try:
                        item_quantity = float(prop.mention_text)
                    except ValueError:
                        pass
                elif prop.type == "price":
                    try:
                        item_price = float(prop.mention_text)
                    except ValueError:
                        pass
            if item_description or item_quantity or item_price:
                items.append(Item(description=item_description, quantity=item_quantity, price=item_price))

    return Receipt(merchant=merchant_name, tax=tax_amount, total=total_amount, items=items)
