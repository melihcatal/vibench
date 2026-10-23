import boto3

class DocumentClient:
    def __init__(self):
        self.textract_client = boto3.client('textract')

    def extract_text(self, document):
        response = self.textract_client.detect_document_text(Document={'Bytes': document})
        text = ''
        for item in response['Blocks']:
            if item['BlockType'] == 'LINE':
                text += item['Text'] + '\n'
        return text