import os
from typing import Dict, Any, List
from document_client import DocumentAIClient
from document_models import DocumentExtractionResult, ExtractedField, ExtractedLineItem

def extract_receipt_fields(document_content: bytes, mime_type: str) -> DocumentExtractionResult:
    client = DocumentAIClient()
    # Use a pre-trained receipt parser for Google Document AI
    receipt_processor_id = os.environ.get("GOOGLE_DOCUMENT_AI_RECEIPT_PROCESSOR_ID", "builtin/receipt")
    document = client.process_document(receipt_processor_id, document_content, mime_type)

    extracted_fields: Dict[str, ExtractedField] = {}
    extracted_line_items: List[ExtractedLineItem] = []

    for entity in document.entities:
        field_name = entity.type_
        field_value = entity.mention_text if entity.mention_text else entity.normalized_value.text if entity.normalized_value else None
        confidence = entity.confidence
        bounding_boxes = []
        if entity.page_anchor.page_refs:
            for page_ref in entity.page_anchor.page_refs:
                for segment in page_ref.bounding_poly.normalized_vertices:
                    bounding_boxes.append([segment.x, segment.y])

        extracted_fields[field_name] = ExtractedField(
            name=field_name,
            value=field_value,
            confidence=confidence,
            bounding_boxes=bounding_boxes
        )

        if field_name == "line_item":
            item_description = None
            item_quantity = None
            item_unit_price = None
            item_total_price = None

            for prop in entity.properties:
                if prop.type_ == "description":
                    item_description = prop.mention_text
                elif prop.type_ == "quantity":
                    item_quantity = float(prop.normalized_value.text) if prop.normalized_value.text else None
                elif prop.type_ == "price": # Document AI often calls total price 'price' for receipt line items
                    item_total_price = float(prop.normalized_value.text) if prop.normalized_value.text else None
                elif prop.type_ == "unit_price":
                    item_unit_price = float(prop.normalized_value.text) if prop.normalized_value.text else None
            
            if item_description or item_quantity or item_unit_price or item_total_price:
                extracted_line_items.append(ExtractedLineItem(
                    description=item_description,
                    quantity=item_quantity,
                    unit_price=item_unit_price,
                    total_price=item_total_price
                ))

    return DocumentExtractionResult(
        document_type="RECEIPT",
        fields=extracted_fields,
        line_items=extracted_line_items
    )
