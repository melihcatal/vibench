import boto3


def extract_fields(document_text):
    textract = boto3.client("textract")
    response = textract.analyze_expense(DocumentText=document_text)
    return response
