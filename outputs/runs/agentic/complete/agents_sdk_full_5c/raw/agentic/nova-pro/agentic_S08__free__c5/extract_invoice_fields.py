import boto3

def extract_invoice_fields(document):
    textract = boto3.client('textract')
    response = textract.analyze_document(Document={'Bytes': document}, FeatureTypes=['FORMS'])
    # Extract fields logic here