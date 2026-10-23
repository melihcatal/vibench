import boto3

def extract_text(document_path):
    textract = boto3.client('textract')
    with open(document_path, 'rb') as document:
        response = textract.detect_document_text(Document={'Bytes': document.read()})
    text = ' '.join([item['Text'] for block in response['Blocks'] if block['BlockType'] == 'LINE' for item in block['Relationships'] if item['Type'] == 'CHILD' for child in response['Blocks'] if child['Id'] == item['Ids'][0] and child['BlockType'] == 'WORD'])
    return text