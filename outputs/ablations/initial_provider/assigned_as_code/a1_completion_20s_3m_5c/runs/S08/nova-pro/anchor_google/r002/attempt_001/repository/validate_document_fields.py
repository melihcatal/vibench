import boto3

def validate_document_fields(extracted_fields):
    required_fields = ['vendor', 'date', 'total']
    for field in required_fields:
        if field not in extracted_fields or not extracted_fields[field]:
            return False
    return True