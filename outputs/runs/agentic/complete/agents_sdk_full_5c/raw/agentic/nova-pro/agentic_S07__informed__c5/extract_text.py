import boto3

def extract_text(document):
    textract = boto3.client('textract')
    response = textract.detect_document_text(Document={'Bytes': document})
    return response['Blocks']