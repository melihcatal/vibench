from google.cloud import documentai_v1beta3 as documentai
from google.api_core.client_options import ClientOptions

def extract_invoice_fields(project_id: str, location: str, processor_id: str, file_path: str) -> dict:
    """
    Extracts vendor, date, total, and line-item fields from an invoice using Google Cloud Document AI.
    """

    # You can set the api_endpoint based on your processor's location
    client_options = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    client = documentai.DocumentProcessorServiceClient(client_options=client_options)

    name = client.processor_path(project_id, location, processor_id)

    with open(file_path, "rb") as image:
        image_content = image.read()

    raw_document = documentai.RawDocument(content=image_content, mime_type="application/pdf")

    # Configure the process request
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)

    result = client.process_document(request=request)
    document = result.document

    extracted_data = {
        "vendor": None,
        "date": None,
        "total": None,
        "line_items": []
    }

    # Extract fields from the document
    for entity in document.entities:
        if entity.type_ == "supplier_name":
            extracted_data["vendor"] = entity.mention_text
        elif entity.type_ == "invoice_date":
            extracted_data["date"] = entity.mention_text
        elif entity.type_ == "total_amount":
            extracted_data["total"] = entity.mention_text
        elif entity.type_ == "line_item":
            line_item = {}
            for prop in entity.properties:
                if prop.type_ == "description":
                    line_item["description"] = prop.mention_text
                elif prop.type_ == "amount":
                    line_item["amount"] = prop.mention_text
                elif prop.type_ == "quantity":
                    line_item["quantity"] = prop.mention_text
            if line_item:
                extracted_data["line_items"].append(line_item)

    return extracted_data
