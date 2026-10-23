import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from document_client import load_image_bytes

def extract_receipt_fields(image_path: str) -> dict:
    endpoint = os.getenv('AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT')
    key = os.getenv('AZURE_DOCUMENT_INTELLIGENCE_KEY')
    if not endpoint or not key:
        return {'error': 'Missing Azure env vars'}
    client = DocumentIntelligenceClient(endpoint, AzureKeyCredential(key))
    image_bytes = load_image_bytes(image_path)
    poller = client.begin_analyze_document("prebuilt-receipt", document=image_bytes)
    result = poller.result()
    if result.documents is None or not result.documents:
        return {'error': 'No document analyzed'}
    fields_dict = result.documents[0].fields.to_dict()
    merchant = fields_dict.get('MerchantName', {}).get('content')
    date_str = fields_dict.get('TransactionDate', {}).get('content')
    total = float(fields_dict.get('Total', {}).get('content') or 0)
    tax_total = fields_dict.get('TotalTax', {}).get('content')
    tax = float(tax_total) if tax_total else None
    items = []
    items_field = fields_dict.get('Items')
    if items_field and 'value' in items_field:
        for item in items_field['value']:
            item_dict = {}
            for k, v in item.items():
                if isinstance(v, dict) and 'content' in v:
                    item_dict[k] = v['content']
            items.append(item_dict)
    confs = {}
    for fname, fval in fields_dict.items():
        if isinstance(fval, dict) and 'confidence' in fval:
            confs[fname] = fval['confidence']
    result = {
        'merchant': merchant,
        'date': date_str,
        'total': total,
        'tax': tax,
        'items': items,
        'field_confidences': confs
    }
    return result