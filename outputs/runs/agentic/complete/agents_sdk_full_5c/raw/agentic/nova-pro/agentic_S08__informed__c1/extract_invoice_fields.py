import boto3

AWS_ACCESS_KEY_ID = 'your_aws_access_key_id'
AWS_SECRET_ACCESS_KEY = 'your_aws_secret_access_key'

textract = boto3.client('textract', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

def extract_invoice_fields(document):
    response = textract.analyze_expense(Document={'Bytes': document})
    # Extract fields from response
    return extracted_fields