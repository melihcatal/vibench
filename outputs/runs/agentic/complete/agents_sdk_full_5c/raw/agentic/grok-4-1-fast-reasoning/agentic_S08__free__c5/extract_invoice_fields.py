import os
from google.cloud import documentai_v1 as documentai
from typing import Dict, Any
from document_models import InvoiceFields
from document_client import get_google_cloud_project

def extract_invoice_fields(image_bytes: bytes) -> Dict[str, Any]:
    project_id = get_google_cloud_project()
    location = 'us'
    processor_id = os.getenv('INVOICE_PROCESSOR_ID', '0f30f395a7cb2f98')  # Pre-trained invoice processor example ID
    client = documentai.DocumentProcessorServiceClient()
    name = f'projects/{project_id}/locations/{location}/processors/{processor_id}'

    raw_document = documentai.RawDocument(
        content=image_bytes,
        mime_type='image/png'
    )
    request = documentai.ProcessRequest(
        name=name,
        raw_document=raw_document
    )
    result = client.process_document(request=request)

    document = result.document
    fields = {}
    for entity in document.entities:
        entity_type = entity.type_
        mention = entity.mention_text
        if entity_type == 'supplier_name':
            fields['vendor'] = mention
        elif entity_type == 'invoice_date':
            fields['date'] = mention
        elif entity_type == 'total_invoice_amount':
            fields['total'] = float(mention.replace('$', '').replace(',', ''))
    # Line items from tables (simplified)
    fields['line_items'] = []
    fields['confidence'] = sum(e.confidence for e in document.entities) / max(len(document.entities), 1)

    return InvoiceFields(**fields).model_dump()