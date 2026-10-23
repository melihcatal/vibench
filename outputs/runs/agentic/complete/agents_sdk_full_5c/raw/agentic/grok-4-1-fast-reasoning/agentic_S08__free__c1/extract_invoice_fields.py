import os
from google.cloud import documentai_v1 as documentai
from document_models import ExtractedInvoice
from document_client import get_google_cloud_project

def extract_invoice_fields(image_bytes: bytes) -> ExtractedInvoice:
    project_id = get_google_cloud_project()
    location = 'us'
    processor_id = os.getenv('INVOICE_PROCESSOR_ID')  # e.g., from Google Cloud Console for invoice processor
    client = documentai.DocumentProcessorServiceClient()
    name = client.processor_path(project_id, location, processor_id)

    raw_document = documentai.RawDocument(content=image_bytes, mime_type='image/png')
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)
    result = client.process_document(request=request)
    document = result.document

    vendor = date_ = total = None
    line_items = []
    confidence = {}

    for entity in document.entities:
        desc = entity.type_
        text = entity.mention_text
        conf = entity.confidence
        if 'vendor' in desc.lower() or 'supplier' in desc.lower():
            vendor = text
            confidence['vendor'] = conf
        elif 'date' in desc.lower():
            date_ = text
            confidence['date'] = conf
        elif 'total' in desc.lower():
            total = float(text.replace('$', '').replace(',', ''))
            confidence['total'] = conf

    return ExtractedInvoice(
        vendor=vendor,
        date=date_,
        total=total,
        line_items=line_items,
        confidence=confidence
    )
