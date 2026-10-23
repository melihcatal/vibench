import os
import boto3

def extract_fields(document_path):
    client = boto3.client('textract', region_name='us-west-2', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
    with open(document_path, 'rb') as document_file:
        response = client.analyze_document(Document={'Bytes': document_file.read()}, FeatureTypes=['FORMS'])
        return response['Blocks']