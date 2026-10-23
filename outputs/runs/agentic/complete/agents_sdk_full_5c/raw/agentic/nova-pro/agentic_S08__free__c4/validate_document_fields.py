import boto3

textract_client = boto3.client('textract')

def validate_document_fields(extracted_fields):
    # Validation logic here
    return is_valid