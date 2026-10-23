import boto3

def extract_key_values(image_path):
    client = boto3.client('textract')
    with open(image_path, 'rb') as image:
        response = client.analyze_document(Document={'Bytes': image.read()}, FeatureTypes=['FORMS'])
    key_values = {block['KeyDetection']['Text']: block['ValueDetection']['Text'] for block in response['Blocks'] if block['BlockType'] == 'KEY_VALUE_SET'}
    return key_values