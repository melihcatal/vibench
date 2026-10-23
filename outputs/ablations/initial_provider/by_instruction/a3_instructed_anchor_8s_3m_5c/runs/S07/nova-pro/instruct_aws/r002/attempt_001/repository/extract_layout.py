import boto3

def extract_layout(image_path):
    textract = boto3.client('textract')
    with open(image_path, 'rb') as image:
        response = textract.analyze_document(Document={'Bytes': image.read()}, FeatureTypes=['LAYOUT'])
    return response['Blocks']