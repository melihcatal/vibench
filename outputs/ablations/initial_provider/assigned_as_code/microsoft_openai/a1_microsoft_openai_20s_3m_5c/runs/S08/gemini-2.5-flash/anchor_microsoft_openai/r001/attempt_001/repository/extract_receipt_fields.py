import io
from document_client import DocumentClient
from document_models import ExtractedDocument, LineItem

def extract_receipt_fields(payload):
    document_client = DocumentClient().get_client()
    with document_client as client:
        result = client.begin_analyze_document('prebuilt-receipt',
            body=io.BytesIO(payload['document_bytes']), content_type=payload['mime_type']).result()

    extracted_receipts = []
    for document in result.documents or []:
        fields = document.fields or {}

        def get_field_value(field_name, default=None):
            field = fields.get(field_name)
            if field and field.content is not None:
                return field.content
            return default
        
        def get_field_float_value(field_name, default=None):
            field = fields.get(field_name)
            if field and field.value_number is not None:
                return float(field.value_number)
            return default
        
        def get_field_confidence(field_name):
            field = fields.get(field_name)
            return field.confidence if field else 0.0

        items = fields.get('Items')
        line_items = []
        for item in (items.value_array or []) if items else []:
            values = item.value_object or {}
            line_items.append(LineItem(
                description=get_field_value('Description'),
                quantity=get_field_float_value('Quantity'),
                amount=get_field_float_value('TotalPrice')
            ))

        confidence_scores = {
            "merchant_name": get_field_confidence('MerchantName'),
            "total": get_field_confidence('Total'),
            "tax": get_field_confidence('TotalTax')
        }

        extracted_receipts.append(ExtractedDocument(
            merchant_name=get_field_value('MerchantName'),
            total=get_field_float_value('Total'),
            tax=get_field_float_value('TotalTax'),
            date=get_field_value('TransactionDate'),
            items=line_items,
            confidence=confidence_scores
        ))
    return {'receipts': extracted_receipts}
