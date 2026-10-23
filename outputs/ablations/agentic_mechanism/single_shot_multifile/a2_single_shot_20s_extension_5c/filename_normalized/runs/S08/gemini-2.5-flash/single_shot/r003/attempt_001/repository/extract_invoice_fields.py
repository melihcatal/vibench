import os
from google.cloud import documentai_v1 as documentai
from document_client import get_document_ai_client
from document_models import DocumentExtractionRequest, NormalizedExpense, LineItem
from typing import Dict, Any, List, Optional

def extract_invoice_fields(request: DocumentExtractionRequest) -> NormalizedExpense:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us")
    processor_id = os.environ.get("GOOGLE_CLOUD_INVOICE_PROCESSOR_ID", "invoice-parser")

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set")

    client = get_document_ai_client()
    name = client.processor_path(project_id, location, processor_id)

    raw_document = documentai.RawDocument(
        content=request.document_bytes,
        mime_type=request.mime_type,
    )

    request_docai = documentai.ProcessRequest(name=name, raw_document=raw_document)
    response = client.process_document(request=request_docai)
    document = response.document

    vendor_name: Optional[str] = None
    transaction_date: Optional[str] = None
    total_amount: Optional[float] = None
    currency: Optional[str] = None
    tax_amount: Optional[float] = None
    extracted_line_items: List[LineItem] = []
    confidence_scores: List[float] = []
    notes: Optional[str] = None

    for entity in document.entities:
        if entity.type_ == "vendor_name":
            vendor_name = entity.mention_text
            confidence_scores.append(entity.confidence)
        elif entity.type_ == "date":
            transaction_date = entity.mention_text
            confidence_scores.append(entity.confidence)
        elif entity.type_ == "total_amount":
            if entity.normalized_value and entity.normalized_value.money_value:
                total_amount = float(entity.normalized_value.money_value.units) + (
                    float(entity.normalized_value.money_value.nanos) / 1_000_000_000
                ) if entity.normalized_value.money_value.nanos is not None else float(entity.normalized_value.money_value.units)
                currency = entity.normalized_value.money_value.currency_code
            elif entity.mention_text:
                try:
                    total_amount = float(entity.mention_text.replace("$", "").replace(",", ""))
                except ValueError:
                    pass
            confidence_scores.append(entity.confidence)
        elif entity.type_ == "tax":
            if entity.normalized_value and entity.normalized_value.money_value:
                tax_amount = float(entity.normalized_value.money_value.units) + (
                    float(entity.normalized_value.money_value.nanos) / 1_000_000_000
                ) if entity.normalized_value.money_value.nanos is not None else float(entity.normalized_value.money_value.units)
            elif entity.mention_text:
                try:
                    tax_amount = float(entity.mention_text.replace("$", "").replace(",", ""))
                except ValueError:
                    pass
            confidence_scores.append(entity.confidence)
        elif entity.type_ == "line_item":
            item_description: Optional[str] = None
            item_quantity: Optional[float] = None
            item_unit_price: Optional[float] = None
            item_total_price: Optional[float] = None
            
            for prop in entity.properties:
                if prop.type_ == "description":
                    item_description = prop.mention_text
                elif prop.type_ == "quantity":
                    try:
                        item_quantity = float(prop.mention_text)
                    except ValueError:
                        pass
                elif prop.type_ == "unit_price":
                    if prop.normalized_value and prop.normalized_value.money_value:
                        item_unit_price = float(prop.normalized_value.money_value.units) + (
                            float(prop.normalized_value.money_value.nanos) / 1_000_000_000
                        ) if prop.normalized_value.money_value.nanos is not None else float(prop.normalized_value.money_value.units)
                    elif prop.mention_text:
                        try:
                            item_unit_price = float(prop.mention_text.replace("$", "").replace(",", ""))
                        except ValueError:
                            pass
                elif prop.type_ == "amount":
                    if prop.normalized_value and prop.normalized_value.money_value:
                        item_total_price = float(prop.normalized_value.money_value.units) + (
                            float(prop.normalized_value.money_value.nanos) / 1_000_000_000
                        ) if prop.normalized_value.money_value.nanos is not None else float(prop.normalized_value.money_value.units)
                    elif prop.mention_text:
                        try:
                            item_total_price = float(prop.mention_text.replace("$", "").replace(",", ""))
                        except ValueError:
                            pass
            
            extracted_line_items.append(
                LineItem(
                    description=item_description,
                    quantity=item_quantity,
                    unit_price=item_unit_price,
                    total_price=item_total_price,
                )
            )
            confidence_scores.append(entity.confidence)
        elif entity.type_ == "notes":
            notes = entity.mention_text
            confidence_scores.append(entity.confidence)

    overall_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else None

    raw_extraction_data = {}
    for entity in document.entities:
        raw_extraction_data[entity.type_] = {
            "mention_text": entity.mention_text,
            "confidence": entity.confidence,
            "normalized_value": str(entity.normalized_value) if entity.normalized_value else None,
            "properties": [{p.type_: p.mention_text} for p in entity.properties]
        }

    return NormalizedExpense(
        vendor_name=vendor_name,
        transaction_date=transaction_date,
        total_amount=total_amount,
        currency=currency,
        tax_amount=tax_amount,
        line_items=extracted_line_items,
        document_type="invoice",
        confidence_score=overall_confidence,
        raw_extraction=raw_extraction_data,
        notes=notes,
    )