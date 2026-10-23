import os
from google.cloud import documentai_v1beta3 as documentai
from document_client import get_document_ai_client
from document_models import ExtractedInvoiceFields, LineItem


def extract_invoice_fields(
    project_id: str, location: str, processor_id: str, file_content: bytes
) -> ExtractedInvoiceFields:
    """
    Extracts vendor, date, total, and line-item fields from an invoice using Google Document AI.
    The processor_id should correspond to an Invoice Parser processor.
    """
    client = get_document_ai_client()

    # The full resource name of the processor
    # e.g., projects/project_id/locations/location/processors/processor_id
    resource_name = client.processor_path(project_id, location, processor_id)

    # Refer to https://cloud.google.com/document-ai/docs/reference/rest/v1beta3/Document#MimeType
    document = documentai.Document(
        content=file_content, mime_type="application/pdf"
    )  # Assuming PDF input

    request = documentai.ProcessRequest(name=resource_name, document=document)

    result = client.process_document(request=request)
    document_response = result.document

    # Initialize with default values
    extracted_fields = ExtractedInvoiceFields()

    if document_response.entities:
        for entity in document_response.entities:
            if entity.type == "vendor_name":
                extracted_fields.vendor_name = entity.mention_text
                extracted_fields.confidence = max(
                    extracted_fields.confidence, entity.confidence
                )
            elif entity.type == "invoice_date":
                extracted_fields.invoice_date = entity.mention_text
                extracted_fields.confidence = max(
                    extracted_fields.confidence, entity.confidence
                )
            elif entity.type == "total_amount":
                # Assuming total_amount is a number and can be converted to float
                try:
                    extracted_fields.total_amount = float(entity.mention_text)
                    extracted_fields.confidence = max(
                        extracted_fields.confidence, entity.confidence
                    )
                except ValueError:
                    pass  # Handle cases where conversion fails
            elif entity.type == "line_item" and entity.properties:
                line_item = LineItem(description="")
                for prop in entity.properties:
                    if prop.type == "description":
                        line_item.description = prop.mention_text
                    elif prop.type == "quantity":
                        try:
                            line_item.quantity = float(prop.mention_text)
                        except ValueError:
                            pass
                    elif prop.type == "unit_price":
                        try:
                            line_item.unit_price = float(prop.mention_text)
                        except ValueError:
                            pass
                    elif prop.type == "total_price":
                        try:
                            line_item.total_price = float(prop.mention_text)
                        except ValueError:
                            pass
                extracted_fields.line_items.append(line_item)

    return extracted_fields
