import boto3

textract = boto3.client('textract')

def summarize_invoice(document_location):
    response = textract.analyze_document(
        Document={'S3Object':{'Bucket':document_location['Bucket'], 'Name':document_location['Name']}},
        FeatureTypes=['FORMS'])
    # Summarize logic here
    return summary