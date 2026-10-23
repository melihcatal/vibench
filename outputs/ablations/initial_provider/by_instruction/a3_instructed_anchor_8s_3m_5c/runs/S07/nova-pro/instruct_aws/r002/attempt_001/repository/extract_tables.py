import boto3

def extract_tables(image_path):
    textract = boto3.client('textract')
    with open(image_path, 'rb') as image:
        response = textract.analyze_document(Document={'Bytes': image.read()}, FeatureTypes=['TABLES'])
    return response['Blocks']