import boto3

def get_textract_client():
    return boto3.client('textract')

def get_document_bytes(document_path):
    with open(document_path, 'rb') as document:
        return document.read())