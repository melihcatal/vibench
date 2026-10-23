import os
from google.cloud import documentai_v1 as documentai
from google.api_core.client_options import ClientOptions
from document_models import InvoiceExtractionResult, LineItem

def extract_invoice_fields(project_id: str, location: str, processor_id: str, file_content: bytes) -> InvoiceExtractionResult:
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    client = documentai.DocumentProcessorServiceClient(client_options=opts)
    resource_name = client.processor_path(project_id, location, processor_id)

    document = documentai.RawDocument(content=file_content, mime_type="application/pdf")
    request = documentai.ProcessRequest(name=resource_name, raw_document=document)
    result = client.process_document(request=request)
    document_proto = result.document

    vendor_name = ""
    invoice_date = ""
    total_amount = 0.0
    line_items = []

    for entity in document_proto.entities:
        if entity.type == "vendor_name" and entity.mention_text:
            vendor_name = entity.mention_text
        elif entity.type == "invoice_date" and entity.mention_text:
            invoice_date = entity.mention_text
        elif entity.type == "total_amount" and entity.mention_text:
            try:
                total_amount = float(entity.mention_text.replace(",", ""))
            except ValueError:
                pass # Handle cases where conversion fails

        if entity.type == "line_item":
            item_description = ""
            item_amount = 0.0
            for prop in entity.properties:
                if prop.type == "description" and prop.mention_text:
                    item_description = prop.mention_text
                elif prop.type == "amount" and prop.mention_text:
                    try:
                        item_amount = float(prop.mention_text.replace(",", ""))
                    except ValueError:
                        pass
            if item_description or item_amount:
                line_items.append(LineItem(description=item_description, amount=item_amount))

    return InvoiceExtractionResult(
        vendor=vendor_name,
        date=invoice_date,
        total=total_amount,
        line_items=line_items
    )

if __name__ == '__main__':
    # Example usage:
    # PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
    # LOCATION = "us" # e.g., "us"
    # PROCESSOR_ID = "YOUR_PROCESSOR_ID" # Create an Invoice Parser processor in Document AI
    # with open("invoice.pdf", "rb") as f:
    #     content = f.read()
    # result = extract_invoice_fields(PROJECT_ID, LOCATION, PROCESSOR_ID, content)
    # print(result.model_dump_json(indent=2))
    pass
