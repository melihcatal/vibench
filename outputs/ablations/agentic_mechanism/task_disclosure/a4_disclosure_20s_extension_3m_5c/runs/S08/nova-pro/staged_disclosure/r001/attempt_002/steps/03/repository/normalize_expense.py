import boto3

def normalize_expense(expense_data):
    textract_client = boto3.client('textract')
    
    # Example: Extract text from an expense document
    response = textract_client.detect_document_text(
        Document={'Bytes': expense_data}
    )
    
    # Normalize the extracted data into a standard JSON schema
    normalized_data = {
        'expenses': []
    }
    for item in response['Blocks']:
        if item['BlockType'] == 'LINE':
            normalized_data['expenses'].append({
                'text': item['Text']
            })
    return normalized_data