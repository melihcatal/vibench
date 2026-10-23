import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

def configure_aws(region_name='us-west-2'):
    """Configure AWS client with specified region"""
    try:
        session = boto3.Session(region_name=region_name)
        textract_client = session.client('textract')
        return textract_client
    except (NoCredentialsError, PartialCredentialsError) as e:
        raise Exception('AWS credentials not found or incomplete')

def extract_text(document_path):
    """Extract text from a document using Amazon Textract"""
    textract_client = configure_aws()
    with open(document_path, 'rb') as document:
        response = textract_client.detect_document_text(Document={'Bytes': document.read()})
        return response

def extract_layout(document_path):
    """Extract layout from a document using Amazon Textract"""
    textract_client = configure_aws()
    with open(document_path, 'rb') as document:
        response = textract_client.analyze_document(Document={'Bytes': document.read()}, FeatureTypes=['LAYOUT'])
        return response