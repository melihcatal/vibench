import boto3

def extract_layout(image_path):
    textract_client = boto3.client('textract')
    with open(image_path, 'rb') as image:
        response = textract_client.analyze_document(Document={'Bytes': image.read()}, FeatureTypes=['TABLES', 'FORMS'])
    return response['Blocks']