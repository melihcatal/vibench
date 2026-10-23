from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
from document_models import value_content
import io


def extract_receipt_fields(payload, config=None):
    config = config or {}
    with DocumentIntelligenceClient(config['endpoint'], AzureKeyCredential(config['api_key'])) as client:
        result = client.begin_analyze_document('prebuilt-receipt', body=io.BytesIO(payload['document_bytes']), content_type=payload['mime_type']).result()
    receipts = []
    for document in result.documents or []:
        fields = document.fields or {}
        items = fields.get('Items')
        extracted_items = []
        for item in (items.value_array or []) if items else []:
            values = item.value_object or {}
            extracted_items.append({'description': value_content(values, 'Description'), 'quantity': value_content(values, 'Quantity'), 'amount': value_content(values, 'Amount')})
        receipts.append({'merchant': value_content(fields, 'MerchantName'), 'tax': value_content(fields, 'TotalTax'), 'total': value_content(fields, 'Total'), 'items': extracted_items})
    return {'receipts': receipts}
