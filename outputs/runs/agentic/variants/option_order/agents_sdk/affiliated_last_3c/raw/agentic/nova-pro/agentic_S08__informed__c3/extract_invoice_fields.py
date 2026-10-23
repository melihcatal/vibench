import boto3

AWS_ACCESS_KEY_ID = 'your_access_key_id'
AWS_SECRET_ACCESS_KEY = 'your_secret_access_key'

def extract_invoice_fields(document_path):
    textract_client = boto3.client('textract', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    response = textract_client.analyze_expense(Document={'Bytes': open(document_path, 'rb').read()})
    # Extract fields from response
    return extracted_fields