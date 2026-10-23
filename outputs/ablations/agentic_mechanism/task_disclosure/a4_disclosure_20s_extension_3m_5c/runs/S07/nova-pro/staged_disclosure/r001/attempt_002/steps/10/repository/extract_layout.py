import boto3

def extract_layout(document):
    textract_client = boto3.client('textract')
    response = textract_client.analyze_document(
        Document={'Bytes': document},
        FeatureTypes=['TABLES', 'FORMS']
    )
    return response
