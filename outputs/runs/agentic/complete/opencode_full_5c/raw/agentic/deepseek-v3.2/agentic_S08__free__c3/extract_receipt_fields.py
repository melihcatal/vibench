import os
from google.cloud import documentai
from google.api_core.client_options import ClientOptions
from document_client import get_documentai_client


def extract_receipt_fields(file_path):
    client = get_documentai_client()

    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "my-project")
    location = os.environ.get("DOCUMENTAI_LOCATION", "us")
    processor_id = os.environ.get(
        "DOCUMENTAI_RECEIPT_PROCESSOR_ID", "receipt-processor"
    )

    processor_name = (
        f"projects/{project_id}/locations/{location}/processors/{processor_id}"
    )

    with open(file_path, "rb") as file:
        file_content = file.read()

    raw_document = documentai.RawDocument(content=file_content, mime_type="image/jpeg")

    request = documentai.ProcessRequest(name=processor_name, raw_document=raw_document)

    result = client.process_document(request=request)
    document = result.document

    extracted_fields = {"merchant": "", "tax": "", "total": "", "items": []}

    for entity in document.entities:
        if entity.type_ == "merchant_name":
            extracted_fields["merchant"] = entity.mention_text
        elif entity.type_ == "tax_amount":
            extracted_fields["tax"] = entity.mention_text
        elif entity.type_ == "total_amount":
            extracted_fields["total"] = entity.mention_text
        elif entity.type_ == "line_item":
            item = {"description": "", "quantity": "", "price": ""}
            for prop in entity.properties:
                if prop.type_ == "line_item/description":
                    item["description"] = prop.mention_text
                elif prop.type_ == "line_item/quantity":
                    item["quantity"] = prop.mention_text
                elif prop.type_ == "line_item/price":
                    item["price"] = prop.mention_text
            extracted_fields["items"].append(item)

    return extracted_fields
