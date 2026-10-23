import boto3

def extract_text(document_path):
    textract = boto3.client('textract')
    with open(document_path, 'rb') as document:
        response = textract.detect_document_text(Document={'Bytes': document.read()})
    return response['Blocks']