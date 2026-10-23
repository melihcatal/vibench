import boto3

textract_client = boto3.client('textract')

def extract_text(document):
    response = textract_client.detect_document_text(Document={'Bytes': document})
    text = ' '.join([item['Text'] for item in response['Blocks'] if item['BlockType'] == 'LINE'])
    return text