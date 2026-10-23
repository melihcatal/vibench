import boto3

def extract_key_values(image_path):
    textract_client = boto3.client('textract')
    with open(image_path, 'rb') as image:
        response = textract_client.analyze_document(Document={'Bytes': image.read()}, FeatureTypes=['FORMS'])
    return response['Blocks']