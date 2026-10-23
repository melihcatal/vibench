import boto3

textract_client = boto3.client('textract')

def extract_receipt_fields(document):
    response = textract_client.analyze_document(
        Document={'Bytes': document},
        FeatureTypes=['FORMS'])
    # Extract fields logic here
    return extracted_fields