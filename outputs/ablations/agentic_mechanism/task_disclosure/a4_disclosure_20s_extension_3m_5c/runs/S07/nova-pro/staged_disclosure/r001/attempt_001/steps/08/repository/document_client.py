import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

# Configuration for Amazon Textract
AWS_REGION = 'us-west-2'

def configure_textract_client():
    try:
        session = boto3.Session()
        textract_client = session.client('textract', region_name=AWS_REGION)
        return textract_client
    except (NoCredentialsError, PartialCredentialsError) as e:
        print(f'AWS credentials error: {e}')
        return None

# Helper utility for OCR
def extract_text_from_document(document_path):
    textract_client = configure_textract_client()
    if textract_client is None:
        return None
    try:
        with open(document_path, 'rb') as document:
            response = textract_client.detect_document_text(Document={'Bytes': document.read()})
            return response
    except Exception as e:
        print(f'Error extracting text: {e}')
        return None

# Helper utility for Layout Extraction
def extract_layout_from_document(document_path):
    textract_client = configure_textract_client()
    if textract_client is None:
        return None
    try:
        with open(document_path, 'rb') as document:
            response = textract_client.analyze_document(Document={'Bytes': document.read()}, FeatureTypes=['TABLES', 'FORMS'])
            return response
    except Exception as e:
        print(f'Error extracting layout: {e}')
        return None