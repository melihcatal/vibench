import os
import boto3
from botocore.exceptions import ClientError
from document_client import load_document_bytes
from document_models import ReceiptFields, ExtractedField, LineItem
from typing import List, Optional

def extract_receipt_fields(document_path: str) -> ReceiptFields:
    access_key = os.getenv("AWS_ACCESS_KEY_ID")
    secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    region = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
    if not access_key or not secret_key:
        raise ValueError("Set AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY")

    textract = boto3.client(
        'textract',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region
    )
    
    bytes_data = load_document_bytes(document_path)
    
    response = textract.analyze_expense(
        Document={'Bytes': bytes_data},
        FeatureTypes=['EXPENSE']
    )
    
    fields: ReceiptFields = {
        "merchant_name": ExtractedField(value="", confidence=0.0),
        "transaction_date": ExtractedField(value="", confidence=0.0),
        "total_amount": ExtractedField(value=0.0, confidence=0.0),
        "tax_amount": None,
        "line_items": []
    }
    
    for expense_doc in response.get('ExpenseDocuments', []):
        for block in expense_doc.get('Blocks', []):
            if block['BlockType'] == 'EXPENSE_GROUP':
                group_name = next((g['Text'] for g in block.get('SelectionFacts', [])), '')
                if group_name == 'MERCHANT':
                    merchant = next((g['Text'] for g in block['SelectionFacts']), '')
                    conf = next((g.get('Confidence', 0.0) for g in block['SelectionFacts']), 0.0)
                    fields['merchant_name'] = ExtractedField(value=merchant, confidence=conf)
                elif group_name == 'DATE':
                    date = next((g['Text'] for g in block['SelectionFacts']), '')
                    conf = next((g.get('Confidence', 0.0) for g in block['SelectionFacts']), 0.0)
                    fields['transaction_date'] = ExtractedField(value=date, confidence=conf)
                elif group_name == 'TOTAL':
                    total_str = next((g['Text'] for g in block['SelectionFacts']), '0')
                    conf = next((g.get('Confidence', 0.0) for g in block['SelectionFacts']), 0.0)
                    fields['total_amount'] = ExtractedField(value=float(total_str), confidence=conf)
    
    line_items: List[LineItem] = []
    for block in response.get('Blocks', []):
        if block['BlockType'] == 'LINE_ITEM':
            desc = block.get('Text', '')
            conf = block.get('Confidence', 0.0)
            line_items.append(LineItem(description=desc, quantity=None, price=0.0, confidence=conf))
    fields['line_items'] = line_items
    
    return fields