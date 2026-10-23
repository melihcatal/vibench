import boto3

def extract_fields(document_path):
    textract = boto3.client('textract')
    with open(document_path, 'rb') as document:
        response = textract.analyze_expense(Document={'Bytes': document.read()})
    return response['ExpenseDocuments']