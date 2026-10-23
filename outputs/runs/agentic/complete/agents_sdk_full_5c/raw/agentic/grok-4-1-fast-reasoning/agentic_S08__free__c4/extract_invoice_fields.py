import boto3
from typing import Dict, Any

def extract_invoice_fields(image_bytes: bytes) -> Dict[str, Any]:
    textract = boto3.client('textract', region_name='us-east-1')
    response = textract.analyze_expense(
        Document={'Bytes': image_bytes},
        FeatureTypes=['INVOICES']
    )
    
    if 'ExpenseDocuments' not in response or not response['ExpenseDocuments']:
        return {}
    
    doc = response['ExpenseDocuments'][0]
    fields: Dict[str, Any] = {}
    
    expense_map = {}
    for field in doc['ExpenseFields']:
        type_name = field['Type']['Text'].upper()
        value = field['Value']['Text']
        conf = field['Confidence']
        expense_map[type_name] = {'value': value, 'confidence': conf}
    
    fields['vendor'] = expense_map.get('VENDOR_NAME', {}).get('value', '')
    fields['date'] = expense_map.get('INVOICE_DATE', {}).get('value', '')
    try:
        fields['total'] = float(expense_map.get('TOTAL', {}).get('value', 0) or 0)
    except ValueError:
        fields['total'] = 0.0
    
    line_items = []
    for line_item in doc.get('LineItems', []):
        li = {}
        for li_field in line_item['LineItemExpenseFields']:
            type_name = li_field['Type']['Text'].lower().replace(' ', '_')
            li[type_name] = li_field['Value']['Text']
        line_items.append(li)
    fields['line_items'] = line_items
    
    fields['confidence'] = {k.lower(): v['confidence'] for k, v in expense_map.items()}
    
    return fields