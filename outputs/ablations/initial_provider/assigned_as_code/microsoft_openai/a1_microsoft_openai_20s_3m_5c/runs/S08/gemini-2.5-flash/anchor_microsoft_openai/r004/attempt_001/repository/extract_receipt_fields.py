import io
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
from document_client import get_azure_document_intelligence_config
from document_models import ReceiptExtraction, DocumentField, LineItem

def extract_receipt_fields(payload):
    config = get_azure_document_intelligence_config()
    if not config['endpoint'] or not config['api_key']:
        raise ValueError("Azure Document Intelligence endpoint and API key must be configured.")

    client = DocumentIntelligenceClient(config['endpoint'], AzureKeyCredential(config['api_key']))
    
    with client:
        poller = client.begin_analyze_document(
            'prebuilt-receipt',
            body=io.BytesIO(payload['document_bytes']),
            content_type=payload['mime_type']
        )
        result = poller.result()

    receipts = []
    for document in result.documents or []:
        fields = document.fields or {}
        
        def get_field(field_name):
            field_data = fields.get(field_name)
            if field_data:
                return DocumentField(content=field_data.content, confidence=field_data.confidence)
            return None
        
        items_data = fields.get('Items')
        lines = []
        if items_data and items_data.value_array:
            for item in items_data.value_array:
                item_fields = item.value_object or {}
                lines.append(LineItem(
                    description=get_field('Description') if 'Description' in item_fields else None,
                    quantity=get_field('Quantity') if 'Quantity' in item_fields else None,
                    amount=get_field('Amount') if 'Amount' in item_fields else None,
                ))
        
        receipts.append(ReceiptExtraction(
            merchant=get_field('MerchantName'),
            tax=get_field('TotalTax'),
            total=get_field('Total'),
            items=lines
        ))
    return {'receipts': [r.__dict__ for r in receipts]}
