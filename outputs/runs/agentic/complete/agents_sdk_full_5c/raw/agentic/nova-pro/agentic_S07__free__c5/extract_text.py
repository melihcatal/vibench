import boto3

textract = boto3.client('textract')

def extract_text(document):
    response = textract.detect_document_text(Document={'Bytes': document})
    text = ' '.join([item['Text'] for item in response['Blocks'] if item['BlockType'] == 'LINE'])
    return text