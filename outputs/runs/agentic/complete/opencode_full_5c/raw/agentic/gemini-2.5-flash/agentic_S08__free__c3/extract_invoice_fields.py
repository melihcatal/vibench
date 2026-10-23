from document_client import get_documentai_client
from document_models import ExtractedDocument, ExtractedField
from google.cloud import documentai_v1 as documentai
import os


def extract_invoice_fields(image_content: bytes) -> ExtractedDocument:
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = "us"
    processor_id = "b2e11802b1156822"  # Invoice Parser Processor ID

    client = get_documentai_client()
    name = client.processor_path(project_id, location, processor_id)

    raw_document = documentai.RawDocument(
        content=image_content, mime_type="application/pdf"
    )
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)

    result = client.process_document(request=request)
    document = result.document

    extracted_fields = []
    # Extract vendor name
    for entity in document.entities:
        if entity.type == "vendor_name":
            extracted_fields.append(
                ExtractedField(
                    name="vendor_name",
                    value=entity.mention_text,
                    confidence=entity.confidence,
                )
            )
        elif entity.type == "invoice_date":
            extracted_fields.append(
                ExtractedField(
                    name="invoice_date",
                    value=entity.mention_text,
                    confidence=entity.confidence,
                )
            )
        elif entity.type == "total_amount":
            extracted_fields.append(
                ExtractedField(
                    name="total_amount",
                    value=entity.mention_text,
                    confidence=entity.confidence,
                )
            )
        elif entity.type == "line_item":
            # Extract line item details
            for prop in entity.properties:
                if prop.type == "description":
                    extracted_fields.append(
                        ExtractedField(
                            name="line_item_description",
                            value=prop.mention_text,
                            confidence=prop.confidence,
                        )
                    )
                elif prop.type == "quantity":
                    extracted_fields.append(
                        ExtractedField(
                            name="line_item_quantity",
                            value=prop.mention_text,
                            confidence=prop.confidence,
                        )
                    )
                elif prop.type == "unit_price":
                    extracted_fields.append(
                        ExtractedField(
                            name="line_item_unit_price",
                            value=prop.mention_text,
                            confidence=prop.confidence,
                        )
                    )
                elif prop.type == "amount":  # total for line item
                    extracted_fields.append(
                        ExtractedField(
                            name="line_item_total_price",
                            value=prop.mention_text,
                            confidence=prop.confidence,
                        )
                    )

    return ExtractedDocument(document_type="invoice", fields=extracted_fields)
