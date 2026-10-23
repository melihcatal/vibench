import os
import boto3
from typing import Dict, Any
from document_models import DocumentFields, LineItem
from document_client import document_bytes_from_path

def extract_receipt_fields(document_input: str | bytes) -> DocumentFields:
    if isinstance(document_input, str):
        document_bytes = document_bytes_from_path(document_input)
    else:
        document_bytes = document_input
    
    session = boto3.Session(
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
    )
    client = session.client('textract')
    
    response = client.analyze_expense(
        Document={'Bytes': document_bytes},
        FeatureTypes=['EXPENSE']
    )
    
    fields_dict: Dict[str, Any] = {"line_items": [], "confidence": {}, "merchant": None}
    
    if 'ExpenseDocuments' in response and response['ExpenseDocuments']:
        exp_doc = response['ExpenseDocuments'][0]
        summary_fields = exp_doc.get('SummaryFields', [])
        
        for field in summary_fields:
            field_type = field['Type']['Text']
            field_text = field['Text']
            conf = field.get('Confidence', 0.0)
            if field_type == 'SUPPLIER_NAME':
                fields_dict['merchant'] = field_text
                fields_dict['confidence']['merchant'] = conf
            elif field_type == 'TAX_TOTAL':
                fields_dict['tax'] = float(field_text)
                fields_dict['confidence']['tax'] = conf
            elif field_type == 'TOTAL':
                fields_dict['total'] = float(field_text)
                fields_dict['confidence']['total'] = conf
        
        # Line items
        for group in exp_doc.get('LineItemGroups', []):
            for line_item in group.get('LineItems', []):
                item_fields = {f['Label']['Text']: f['Text'] for f in line_item['Fields']}
                desc = item_fields.get('DESCRIPTION', 'Unknown')
                price = float(item_fields.get('PRICE', 0))
                line_items.append(LineItem(description=desc, amount=price))
    
    fields_dict['vendor'] = fields_dict['merchant']
    return DocumentFields(**fields_dict)