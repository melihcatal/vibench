import os
from google.cloud import documentai_v1 as documentai
from document_client import load_image, get_google_project
from document_models import InvoiceFields, ExtractedField, LineItem
from typing import List

def extract_invoice_fields(image_path: str) -> InvoiceFields:
    client = documentai.DocumentProcessorServiceClient()
    project_id = get_google_project()
    location = 'us'
    processor_id = os.getenv('INVOICE_PROCESSOR_ID')  # Pre-trained or custom invoice processor ID
    name = client.processor_path(project_id, location, processor_id)

    image_bytes = load_image(image_path)
    raw_document = documentai.RawDocument(
        content=image_bytes,
        mime_type='image/jpeg'
    )

    request = documentai.ProcessRequest(name=name, raw_document=raw_document)
    result = client.process_document(request=request)
    document = result.document

    fields: dict = {}
    line_items: List[LineItem] = []

    for entity in document.entities:
        entity_type = entity.type_
        mention_text = entity.mention_text
        confidence = float(entity.confidence)
        if entity_type == 'supplier_name':
            fields['vendor'] = ExtractedField(value=mention_text, confidence=confidence)
        elif entity_type == 'invoice_date':
            fields['date'] = ExtractedField(value=mention_text, confidence=confidence)
        elif entity_type in ['total_amount', 'invoice_total']:
            value = float(mention_text.replace('$', '').replace(',', ''))
            fields['total'] = ExtractedField(value=value, confidence=confidence)
        elif 'line_item' in entity_type:
            # Simplified line item parsing
            desc = entity.mention_text if 'description' in entity_type else 'Item'
            line_items.append(LineItem(description=desc, quantity=None, unit_price=0.0, total_price=0.0))

    return InvoiceFields(
        vendor=fields.get('vendor', ExtractedField(value='', confidence=0.0)),
        date=fields.get('date', ExtractedField(value='', confidence=0.0)),
        total=fields.get('total', ExtractedField(value=0.0, confidence=0.0)),
        line_items=line_items
    )