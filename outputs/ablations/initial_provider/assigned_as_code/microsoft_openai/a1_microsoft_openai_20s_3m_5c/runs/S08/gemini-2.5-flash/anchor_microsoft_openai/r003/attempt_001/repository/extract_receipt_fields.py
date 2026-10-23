from document_client import DocumentAIManager
from document_models import ExtractedReceipt, ExtractedLineItem
from typing import Dict, Any
import os


def extract_receipt_fields(payload: Dict[str, Any], config: Dict[str, Any] = None) -> Dict[str, Any]:
    config = config or {}
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID", config.get("project_id"))
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", config.get("location", "us"))
    processor_id = os.environ.get("GOOGLE_CLOUD_DOCUMENTAI_RECEIPT_PROCESSOR_ID", config.get("receipt_processor_id"))

    if not all([project_id, location, processor_id]):
        raise ValueError("Missing GOOGLE_CLOUD_PROJECT_ID, GOOGLE_CLOUD_LOCATION, or GOOGLE_CLOUD_DOCUMENTAI_RECEIPT_PROCESSOR_ID environment variables or config values.")

    doc_manager = DocumentAIManager(project_id, location)
    document = doc_manager.process_document(processor_id, payload['document_bytes'], payload['mime_type'])

    extracted_receipt = ExtractedReceipt()

    if document.entities:
        for entity in document.entities:
            if entity.type == "merchant_name":
                extracted_receipt.merchant = entity.mention_text
            elif entity.type == "total_amount":
                extracted_receipt.total = entity.mention_text
            elif entity.type == "tax_amount":
                extracted_receipt.tax = entity.mention_text
            elif entity.type == "line_item":
                line_item = ExtractedLineItem()
                for prop in entity.properties:
                    if prop.type == "description":
                        line_item.description = prop.mention_text
                    elif prop.type == "quantity":
                        line_item.quantity = prop.mention_text
                    elif prop.type == "amount":
                        line_item.amount = prop.mention_text
                extracted_receipt.items.append(line_item)

    return extracted_receipt.model_dump()
