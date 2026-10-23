import boto3

# Configuration for Amazon Textract
AWS_REGION = 'us-west-2'

# Create a low-level service client
textract_client = boto3.client('textract', region_name=AWS_REGION)

def configure_textract_client(region_name):
    global textract_client
    textract_client = boto3.client('textract', region_name=region_name)

def perform_ocr(document):
    response = textract_client.detect_document_text(Document={'Bytes': document})
    return response

def perform_layout_extraction(document):
    response = textract_client.analyze_document(Document={'Bytes': document}, FeatureTypes=['TABLES', 'FORMS'])
    return response