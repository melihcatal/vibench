from google.cloud import documentai_v1 as documentai
import os
from typing import Dict, Any
from document_client import image_bytes_to_base64

def extract_receipt_fields(image_bytes: bytes) -> Dict[str, Any]:
    client = documentai.DocumentProcessorServiceClient()
    processor_name = os.getenv('DOCUMENTAI_RECEIPT_PROCESSOR')
    
    b64_image = image_bytes_to_base64(image_bytes)
    raw_document = documentai.RawDocument(
        content=b64_image, 
        mime_type='image/jpeg'  # or detect
    )
    
    request = documentai.ProcessRequest(
        name=processor_name,
        raw_document=raw_document,
    )
    
    result = client.process_document(request=request)
    document = result.document
    
    fields: Dict[str, Any] = {}
    confidences = {}
    
    for entity in document.entities:
        entity_type = entity.type_
        mention = entity.mention_text
        conf = entity.confidence
        
        if entity_type == 'merchant_name' or entity_type == 'merchant':
            fields['merchant'] = mention
        elif entity_type == 'total_price' or entity_type == 'total_amount':
            try:
                fields['total'] = float(mention.replace('$', '').replace(',', ''))
            except:
                fields['total'] = 0.0
        elif entity_type == 'tax_amount':
            try:
                fields['tax'] = float(mention.replace('$', '').replace(',', ''))
            except:
                pass
        elif entity_type == 'transaction_date':
            fields['date'] = mention
        
        if entity_type in fields:
            confidences[entity_type] = conf
    
    # simplistic items from blocks
    items = []
    for page in document.pages:
        for block in page.blocks:
            if block.block_type == 1:  # paragraph
                items.append(block.layout.text_anchor.content)
    fields['items'] = [i.strip() for i in items if i.strip()][:10]
    
    fields['confidence'] = confidences
    
    return fields