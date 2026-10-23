import boto3

def normalize_expense(expense_data):
    textract_client = boto3.client('textract')
    response = textract_client.analyze_expense_document(
        Document={'Bytes': expense_data}
    )
    normalized_data = {}
    for block in response['Blocks']:
        if block['BlockType'] == 'LINE':
            normalized_data[block['Text']] = block['Confidence']
    return normalized_data

if __name__ == '__main__':
    expense_data = b''  # Placeholder for actual expense data
    normalized_expense = normalize_expense(expense_data)
    print(normalized_expense)