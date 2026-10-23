import boto3

def normalize_expense(expense_data):
    textract_client = boto3.client('textract')
    response = textract_client.analyze_expense_document(
        Document={'Bytes': expense_data}
    )
    normalized_expense = {}
    for document in response['ExpenseDocuments']:
        for line_item in document['LineItems']:
            normalized_expense[line_item['LineItemExpenseFields']] = line_item['ValueDetection']['Text']
    return normalized_expense