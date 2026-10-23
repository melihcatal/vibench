import boto3


def detect_image_text(payload, config=None):
    textract = boto3.client('textract', region_name=config['region'], aws_access_key_id=config['aws_access_key_id'], aws_secret_access_key=config['aws_secret_access_key'])
    response = textract.detect_document_text(Document={'Bytes': payload['image_bytes']})
    text = ' '.join([item['Text'] for item in response['Blocks'] if item['BlockType'] == 'LINE'])
    return {'text': text}