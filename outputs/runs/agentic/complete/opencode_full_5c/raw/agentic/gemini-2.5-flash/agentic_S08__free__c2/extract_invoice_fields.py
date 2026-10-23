from google.cloud import documentai_v1beta3 as documentai
import os


def extract_invoice_fields(
    project_id: str, location: str, processor_id: str, file_content: bytes
) -> dict:
    """
    Extracts vendor, date, total, and line-item fields from an invoice using Google Cloud Document AI.
    """
    client = documentai.DocumentProcessorServiceClient()
    processor_name = client.processor_path(project_id, location, processor_id)

    raw_document = documentai.RawDocument(
        content=file_content, mime_type="application/pdf"
    )
    request = documentai.ProcessRequest(name=processor_name, raw_document=raw_document)

    result = client.process_document(request=request)
    document = result.document

    extracted_fields = {
        "vendor_name": None,
        "invoice_date": None,
        "total_amount": None,
        "line_items": [],
    }

    # Example of extracting fields - actual extraction would be more robust
    for entity in document.entities:
        if entity.type == "supplier_name":
            extracted_fields["vendor_name"] = entity.mention_text
        elif entity.type == "invoice_date":
            extracted_fields["invoice_date"] = entity.mention_text
        elif entity.type == "total_amount":
            extracted_fields["total_amount"] = entity.mention_text
        elif entity.type == "line_item":
            item_data = {"description": None, "amount": None, "quantity": None}
            for prop in entity.properties:
                if prop.type == "description":
                    item_data["description"] = prop.mention_text
                elif prop.type == "amount":
                    item_data["amount"] = prop.mention_text
                elif prop.type == "quantity":
                    item_data["quantity"] = prop.mention_text
            extracted_fields["line_items"].append(item_data)

    return extracted_fields
