import boto3
import re

def check_secret_labels(secret_id):
    client = boto3.client('secretsmanager')
    describe_secret_response = client.describe_secret(SecretId=secret_id)
    labels = describe_secret_response['Tags']
    unsafe_labels = [label for label in labels if re.search(r'[^a-zA-Z0-9_]', label)]
    return unsafe_labels