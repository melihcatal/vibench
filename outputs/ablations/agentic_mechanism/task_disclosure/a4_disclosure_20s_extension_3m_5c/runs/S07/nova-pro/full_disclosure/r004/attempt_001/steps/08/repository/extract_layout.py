import boto3

def extract_layout(document):
    textract_client = boto3.client('textract')
    response = textract_client.detect_document_text(Document={'Bytes': document})
    return response
