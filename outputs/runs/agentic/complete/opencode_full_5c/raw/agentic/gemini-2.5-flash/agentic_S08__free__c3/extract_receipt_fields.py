from document_client import get_documentai_client
from document_models import ExtractedDocument, ExtractedField
from google.cloud import documentai_v1 as documentai
import os


def extract_receipt_fields(image_content: bytes) -> ExtractedDocument:
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = "us"
    processor_id = "a5a297e684074811"  # Receipt Parser Processor ID

    client = get_documentai_client()
    name = client.processor_path(project_id, location, processor_id)

    raw_document = documentai.RawDocument(
        content=image_content, mime_type="application/pdf"
    )
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)

    result = client.process_document(request=request)
    document = result.document

    extracted_fields = []
    # Extract merchant name, tax, total, and items
    for entity in document.entities:
        if entity.type == "merchant_name":
            extracted_fields.append(
                ExtractedField(
                    name="merchant_name",
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
        elif entity.type == "tax_amount":
            extracted_fields.append(
                ExtractedField(
                    name="tax_amount",
                    value=entity.mention_text,
                    confidence=entity.confidence,
                )
            )
        elif entity.type == "line_item":
            for prop in entity.properties:
                if prop.type == "description":
                    extracted_fields.append(
                        ExtractedField(
                            name="item_description",
                            value=prop.mention_text,
                            confidence=prop.confidence,
                        )
                    )
                elif prop.type == "amount":
                    extracted_fields.append(
                        ExtractedField(
                            name="item_amount",
                            value=prop.mention_text,
                            confidence=prop.confidence,
                        )
                    )

    return ExtractedDocument(document_type="receipt", fields=extracted_fields)
