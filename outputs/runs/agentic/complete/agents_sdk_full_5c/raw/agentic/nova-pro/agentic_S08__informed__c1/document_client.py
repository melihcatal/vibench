import os

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
MINDEE_API_KEY = os.getenv('MINDEE_API_KEY')

def get_textract_client():
    return boto3.client('textract', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

def get_mindee_client():
    from mindee import InvoiceApi
    return InvoiceApi(api_key=MINDEE_API_KEY)