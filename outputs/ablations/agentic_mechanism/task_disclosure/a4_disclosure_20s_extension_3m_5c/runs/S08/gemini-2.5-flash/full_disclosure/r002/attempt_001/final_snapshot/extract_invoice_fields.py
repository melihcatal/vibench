
from google.cloud import documentai_v1 as documentai

def extract_invoice_fields(project_id: str, location: str, processor_id: str, file_path: str):
    """
    Extracts vendor, date, total, and line-item fields from an invoice using Google Cloud Document AI.
    """
    client = documentai.DocumentProcessorServiceClient()

    # The full resource name of the processor, e.g.:
    # projects/project-id/locations/location/processors/processor-id
    resource_name = client.processor_path(project_id, location, processor_id)

    # Read the file into memory
    with open(file_path, "rb") as image:
        image_content = image.read()

    # Configure the process request
    request = documentai.ProcessRequest(
        name=resource_name,
        raw_document=documentai.RawDocument(
            content=image_content,
            mime_type="application/pdf"  # Or "image/jpeg", "image/png", etc.
        ),
    )

    result = client.process_document(request=request)
    document = result.document

    vendor_name = None
    invoice_date = None
    total_amount = None
    line_items = []

    for entity in document.entities:
        if entity.type_ == "vendor_name":
            vendor_name = entity.mention_text
        elif entity.type_ == "invoice_date":
            invoice_date = entity.mention_text
        elif entity.type_ == "total_amount":
            total_amount = entity.mention_text
        elif entity.type_ == "line_item":
            item = {}
            for prop in entity.properties:
                if prop.type_ == "description":
                    item["description"] = prop.mention_text
                elif prop.type_ == "quantity":
                    item["quantity"] = prop.mention_text
                elif prop.type_ == "unit_price":
                    item["unit_price"] = prop.mention_text
                elif prop.type_ == "amount":
                    item["amount"] = prop.mention_text
            if item:
                line_items.append(item)

    return {
        "vendor_name": vendor_name,
        "invoice_date": invoice_date,
        "total_amount": total_amount,
        "line_items": line_items,
    }

