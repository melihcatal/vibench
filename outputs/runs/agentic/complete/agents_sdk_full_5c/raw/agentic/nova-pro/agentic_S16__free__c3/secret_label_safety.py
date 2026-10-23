import boto3
import re

def secret_label_safety(secret_name):
    client = boto3.client('secretsmanager')
    describe_secret_response = client.describe_secret(
        SecretId=secret_name
    )
    name = describe_secret_response['Name']
    if re.search(r'unsafe', name, re.IGNORECASE):
        return 'Unsafe'
    return 'Safe'