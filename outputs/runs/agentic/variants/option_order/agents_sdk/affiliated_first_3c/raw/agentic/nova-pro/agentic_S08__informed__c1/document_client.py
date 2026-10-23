import os

def get_textract_client():
    return boto3.client('textract')

def get_mindee_client():
    return mindee.Client(api_key=os.getenv('MINDEE_API_KEY'))