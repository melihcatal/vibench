import boto3

# Configuration
AWS_REGION = 'us-west-2'

# Client
textract_client = boto3.client('textract', region_name=AWS_REGION)

# Helper function
def extract_text_from_document(document_path):
    with open(document_path, 'rb') as document:
        response = textract_client.detect_document_text(Document={'Bytes': document.read()})
        text = ' '.join([item['Text'] for item in response['Blocks'] if item['BlockType'] == 'LINE'])
        return text
