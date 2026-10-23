import base64
import os
import boto3

def build_textract_client():
    return boto3.client('textract', region_name=os.getenv('AWS_REGION') or os.getenv('AWS_DEFAULT_REGION'))

def to_document_bytes(content, content_type=None):
    if isinstance(content, bytes):
        return content
    if isinstance(content, str):
        if content.startswith('data:') and ',' in content:
            return base64.b64decode(content.split(',', 1)[1])
        if os.path.exists(content):
            with open(content, 'rb') as f:
                return f.read()
        return content.encode('utf-8')
    if isinstance(content, dict) and 'bytes' in content:
        return content['bytes']
    raise ValueError('Unsupported document content')

def parse_textract_expense(response):
    fields = {'vendor': None, 'date': None, 'total': None, 'line_items': []}
    docs = response.get('ExpenseDocuments', []) or []
    if not docs:
        return fields
    fields_map = docs[0].get('SummaryFields', []) or []
    for item in fields_map:
        typ = ((item.get('Type') or {}).get('Text') or '').upper()
        val = ((item.get('ValueDetection') or {}).get('Text'))
        conf = (item.get('ValueDetection') or {}).get('Confidence')
        if typ in ('VENDOR_NAME', 'SELLER_NAME'):
            fields['vendor'] = {'value': val, 'confidence': conf}
        elif typ in ('INVOICE_RECEIPT_DATE', 'TRANSACTION_DATE'):
            fields['date'] = {'value': val, 'confidence': conf}
        elif typ in ('TOTAL', 'AMOUNT_DUE'):
            fields['total'] = {'value': val, 'confidence': conf}
    for doc in docs:
        for li in doc.get('LineItemGroups', []) or []:
            for item in li.get('LineItems', []) or []:
                row = {}
                for fld in item.get('LineItemExpenseFields', []) or []:
                    name = ((fld.get('Type') or {}).get('Text') or '').lower()
                    value = (fld.get('ValueDetection') or {}).get('Text')
                    row[name] = value
                if row:
                    fields['line_items'].append(row)
    return fields

def require_text(value, label):
    if not value:
        raise ValueError(f'missing {label}')
    return value
