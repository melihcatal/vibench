import boto3

def extract_text(image_path):
    client = boto3.client('textract')
    with open(image_path, 'rb') as image:
        response = client.detect_document_text(Document={'Bytes': image.read()})
    text = ' '.join([item['Text'] for block in response['Blocks'] if block['BlockType'] == 'LINE' for item in block['Relationships'] if item['Type'] == 'CHILD' for child in item['Ids'] for child_block in response['Blocks'] if child_block['Id'] == child and child_block['BlockType'] == 'WORD'])
    return text