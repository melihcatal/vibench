import boto3

def extract_fields(document):
    textract = boto3.client('textract')
    response = textract.analyze_expense(Document={'Bytes': document})
    return response