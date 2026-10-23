import os
import boto3

def extract_fields(text):
    client = boto3.client('comprehend', region_name=os.getenv('AWS_REGION', 'us-west-2'), aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
    entities = client.detect_entities(Text=text, LanguageCode='en')
    return {entity['Text']: entity['Type'] for entity in entities['Entities']}