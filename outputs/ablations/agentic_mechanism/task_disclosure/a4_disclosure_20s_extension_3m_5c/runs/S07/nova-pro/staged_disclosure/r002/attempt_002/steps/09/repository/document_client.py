import boto3

def get_textract_client():
    return boto3.client('textract')

def ocr_layout_extraction(document):
    client = get_textract_client()
    response = client.analyze_document(
        Document={'Bytes': document},
        FeatureTypes=['TABLES', 'FORMS'])
    return response