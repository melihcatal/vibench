import boto3

textract_client = boto3.client('textract')

def normalize_expense(extracted_fields):
    # Normalization logic here
    return normalized_expense