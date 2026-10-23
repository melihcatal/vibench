import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from document_client import load_image_bytes

def extract_invoice_fields(image_path: str) -> dict:
    client = boto3.client('textract')
    image_bytes = load_image_bytes(image_path)
    try:
        response = client.analyze_expense(
            Document={'Bytes': image_bytes},
            FeatureTypes=['EXPENSES']
        )
        if 'ExpenseDocuments' not in response or not response['ExpenseDocuments']:
            return {'error': 'No expense document found'}
        doc = response['ExpenseDocuments'][0]
        expense_fields = {}
        field_confidences = {}
        for ef in doc['ExpenseFields']:
            field_name = ef['Type']['Text']
            value = ef['Value']['Text']
            conf = ef['Confidence']
            expense_fields[field_name] = value
            field_confidences[field_name] = conf
        vendor = None
        for vtype in ['VENDOR_NAME', 'SUPPLIER_NAME', 'INVOICE_VENDOR_NAME']:
            if vtype in expense_fields:
                vendor = expense_fields[vtype]
                break
        date_str = expense_fields.get('INVOICE_DATE')
        total_str = expense_fields.get('TOTAL', '0')
        total = float(total_str) if total_str else 0.0
        line_items = []
        for lig in doc.get('LineItemGroups', []):
            for li in lig.get('LineItems', []):
                item_desc = li['Text']
                item_val_str = li['Value']['Text']
                item_val = float(item_val_str) if item_val_str else 0.0
                line_items.append({
                    'description': item_desc,
                    'amount': item_val
                })
        result = {
            'vendor': vendor,
            'date': date_str,
            'total': total,
            'line_items': line_items,
            'field_confidences': field_confidences
        }
        return result
    except (ClientError, NoCredentialsError) as e:
        return {'error': str(e)}