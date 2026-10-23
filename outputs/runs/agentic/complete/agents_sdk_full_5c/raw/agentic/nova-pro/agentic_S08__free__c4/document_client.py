import boto3

textract_client = boto3.client('textract')

def get_textract_client():
    return textract_client