import boto3

def extract_layout(image_path):
    client = boto3.client('textract')
    with open(image_path, 'rb') as image:
        response = client.analyze_document(Document={'Bytes': image.read()}, FeatureTypes=['LAYOUT'])
    layout = {block['BlockType']: block for block in response['Blocks']}
    return layout