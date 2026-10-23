import boto3

def extract_key_values(image_path):
    textract = boto3.client('textract')
    with open(image_path, 'rb') as image:
        response = textract.analyze_document(Document={'Bytes': image.read()}, FeatureTypes=['FORMS'])
    return response['Blocks']