import boto3

def validate_document_fields(document):
    textract_client = boto3.client('textract')
    # Example validation logic using Textract
    required_fields = ['vendor', 'date', 'total']
    confidence_threshold = 90
    for field in required_fields:
        if field not in document or document[field]['confidence'] < confidence_threshold:
            return False
    return True