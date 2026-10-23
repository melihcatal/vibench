import boto3

def get_textract_client():
    return boto3.client('textract')

def get_translate_client():
    return boto3.client('translate')

def get_comprehend_client():
    return boto3.client('comprehend')