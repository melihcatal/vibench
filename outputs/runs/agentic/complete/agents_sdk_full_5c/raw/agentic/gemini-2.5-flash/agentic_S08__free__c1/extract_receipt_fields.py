import boto3
import os

def extract_receipt_fields(document_content: bytes) -> dict:
    """
    Extracts merchant, tax, total, and items from a receipt using AWS Textract.
    """
    region_name = os.environ.get("AWS_REGION", "us-east-1")
    client = boto3.client('textract', region_name=region_name)

    response = client.analyze_expense(
        Document={
            'Bytes': document_content
        }
    )

    extracted_data = {}
    if 'ExpenseDocuments' in response and len(response['ExpenseDocuments']) > 0:
        expense_doc = response['ExpenseDocuments'][0]

        # Extract summary fields
        for field in expense_doc.get('SummaryFields', []):
            if field.get('Type', {}).get('Text') == 'MERCHANT_NAME':
                extracted_data['merchant_name'] = field.get('ValueDetection', {}).get('Text')
            elif field.get('Type', {}).get('Text') == 'TOTAL':
                extracted_data['total_amount'] = field.get('ValueDetection', {}).get('Text')
            elif field.get('Type', {}).get('Text') == 'TAX':
                extracted_data['tax_amount'] = field.get('ValueDetection', {}).get('Text')
        
        # Extract line items
        if 'LineItemGroups' in expense_doc:
            extracted_data['line_items'] = []
            for group in expense_doc['LineItemGroups']:
                for item in group.get('LineItems', []):
                    line_item = {}
                    for field in item.get('LineItemExpenseFields', []):
                        if field.get('Type', {}).get('Text') == 'ITEM':
                            line_item['description'] = field.get('ValueDetection', {}).get('Text')
                        elif field.get('Type', {}).get('Text') == 'PRICE':
                            line_item['amount'] = field.get('ValueDetection', {}).get('Text')
                    if line_item:
                        extracted_data['line_items'].append(line_item)

    return extracted_data
