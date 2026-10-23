import os
from google.cloud import documentai_v1 as documentai
from google.cloud import storage
from document_client import get_documentai_client
from document_models import NormalizedExpense, LineItem

def extract_invoice_fields(project_id: str, location: str, processor_id: str, file_path: str) -> NormalizedExpense:
    """
    Extracts invoice fields using Google Cloud Document AI.
    """
    client = get_documentai_client()
    processor_name = client.processor_path(project_id, location, processor_id)

    # Read the file into memory
    with open(file_path, "rb") as image:
        image_content = image.read()

    # Create a Document object
    raw_document = documentai.RawDocument(content=image_content, mime_type="application/pdf") # or "image/jpeg", etc.

    # Configure the process request
    request = documentai.ProcessRequest(name=processor_name, raw_document=raw_document)

    # Process the document
    result = client.process_document(request=request)
    document = result.document

    vendor_name = None
    transaction_date = None
    total_amount = None
    currency = None
    invoice_number = None
    line_items = []
    
    vendor_name_confidence = 0.0
    transaction_date_confidence = 0.0
    total_amount_confidence = 0.0
    invoice_number_confidence = 0.0

    # Extract fields
    for entity in document.entities:
        if entity.type == "vendor_name":
            vendor_name = entity.mention_text
            vendor_name_confidence = entity.confidence
        elif entity.type == "date":
            transaction_date = entity.mention_text
            transaction_date_confidence = entity.confidence
        elif entity.type == "total_amount":
            total_amount = float(entity.mention_text) if entity.mention_text else None
            currency = entity.currency_text
            total_amount_confidence = entity.confidence
        elif entity.type == "invoice_id":
            invoice_number = entity.mention_text
            invoice_number_confidence = entity.confidence
        elif entity.type == "line_item":
            item_description = None
            item_quantity = None
            item_unit_price = None
            item_total_price = None
            for prop in entity.properties:
                if prop.type == "description":
                    item_description = prop.mention_text
                elif prop.type == "quantity":
                    item_quantity = float(prop.mention_text) if prop.mention_text else None
                elif prop.type == "unit_price":
                    item_unit_price = float(prop.mention_text) if prop.mention_text else None
                elif prop.type == "amount": # often total for the line item
                    item_total_price = float(prop.mention_text) if prop.mention_text else None
            line_items.append(LineItem(description=item_description, quantity=item_quantity,
                                       unit_price=item_unit_price, total_price=item_total_price))

    confidence_scores = {
        "vendor_name": vendor_name_confidence,
        "transaction_date": transaction_date_confidence,
        "total_amount": total_amount_confidence,
        "invoice_number": invoice_number_confidence,
    }

    return NormalizedExpense(
        document_type="invoice",
        vendor_name=vendor_name,
        transaction_date=transaction_date,
        total_amount=total_amount,
        currency=currency,
        invoice_number=invoice_number,
        line_items=line_items,
        raw_text=document.text,
        confidence_scores=confidence_scores
    )

if __name__ == '__main__':
    # This is an example of how to use the function.
    # Replace with your actual project details and file path.
    # processor_id for "Invoice Parser" might be like 'YOUR_PROCESSOR_ID'
    # project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    # location = "us" # e.g., "us"
    # processor_id = "YOUR_INVOICE_PROCESSOR_ID"
    # file_path = "path/to/your/invoice.pdf"
    #
    # if project_id and location and processor_id and os.path.exists(file_path):
    #     extracted_data = extract_invoice_fields(project_id, location, processor_id, file_path)
    #     print(extracted_data.json(indent=2))
    # else:
    #     print("Please set GOOGLE_CLOUD_PROJECT, provide location, processor_id and a valid file_path.")
    pass
