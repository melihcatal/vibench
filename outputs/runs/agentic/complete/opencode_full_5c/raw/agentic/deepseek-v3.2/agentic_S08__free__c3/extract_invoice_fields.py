import os
from google.cloud import documentai
from google.api_core.client_options import ClientOptions
from document_client import get_documentai_client


def extract_invoice_fields(file_path):
    client = get_documentai_client()

    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "my-project")
    location = os.environ.get("DOCUMENTAI_LOCATION", "us")
    processor_id = os.environ.get(
        "DOCUMENTAI_INVOICE_PROCESSOR_ID", "invoice-processor"
    )

    processor_name = (
        f"projects/{project_id}/locations/{location}/processors/{processor_id}"
    )

    with open(file_path, "rb") as file:
        file_content = file.read()

    raw_document = documentai.RawDocument(
        content=file_content, mime_type="application/pdf"
    )

    request = documentai.ProcessRequest(name=processor_name, raw_document=raw_document)

    result = client.process_document(request=request)
    document = result.document

    extracted_fields = {"vendor": "", "date": "", "total": "", "line_items": []}

    for entity in document.entities:
        if entity.type_ == "supplier_name":
            extracted_fields["vendor"] = entity.mention_text
        elif entity.type_ == "invoice_date":
            extracted_fields["date"] = entity.mention_text
        elif entity.type_ == "total_amount":
            extracted_fields["total"] = entity.mention_text
        elif entity.type_ == "line_item":
            line_item = {
                "description": "",
                "quantity": "",
                "unit_price": "",
                "amount": "",
            }
            for prop in entity.properties:
                if prop.type_ == "line_item/description":
                    line_item["description"] = prop.mention_text
                elif prop.type_ == "line_item/quantity":
                    line_item["quantity"] = prop.mention_text
                elif prop.type_ == "line_item/unit_price":
                    line_item["unit_price"] = prop.mention_text
                elif prop.type_ == "line_item/amount":
                    line_item["amount"] = prop.mention_text
            extracted_fields["line_items"].append(line_item)

    return extracted_fields
