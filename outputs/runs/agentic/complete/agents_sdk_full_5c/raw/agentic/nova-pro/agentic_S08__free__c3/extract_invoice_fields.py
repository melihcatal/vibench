import boto3

textract = boto3.client('textract')

def extract_invoice_fields(document_location):
    response = textract.analyze_document(
        Document={'S3Object':{'Bucket':document_location['Bucket'], 'Name':document_location['Name']}},
        FeatureTypes=['FORMS'])
    # Extract fields logic here
    return extracted_fields