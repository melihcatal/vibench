from google.cloud import documentai
from document_models import DocumentPayload, ReceiptExtractionResult, ExtractedItem
from document_client import get_documentai_client
from typing import Dict, Any, List

def extract_receipt_fields(payload: DocumentPayload, config: Dict[str, Any]) -> ReceiptExtractionResult:
    client = get_documentai_client(config["project_id"], config["location"])
    processor_name = client.processor_path(config["project_id"], config["location"], config["receipt_processor_id"])
    
    raw_document = documentai.RawDocument(
        content=payload.document_bytes, mime_type=payload.mime_type
    )
    request = documentai.ProcessRequest(name=processor_name, raw_document=raw_document)
    
    response = client.process_document(request=request)
    
    merchant = None
    tax = None
    total = None
    items: List[ExtractedItem] = []

    for entity in response.document.entities:
        if entity.type_ == "merchant_name":
            merchant = entity.mention_text
        elif entity.type_ == "total_amount":
            total = entity.mention_text
        elif entity.type_ == "tax_amount":
            tax = entity.mention_text
        elif entity.type_ == "line_item":
            item_values = {p.type_.split("/")[-1]: p.mention_text for p in entity.properties}
            items.append(ExtractedItem(
                description=item_values.get("description"),
                quantity=float(item_values["quantity"]) if item_values.get("quantity") else None,
                amount=float(item_values["amount"]) if item_values.get("amount") else None,
                confidence=entity.confidence
            ))
            
    return ReceiptExtractionResult(
        merchant=merchant,
        tax=tax,
        total=total,
        items=items
    )
