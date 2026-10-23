import json
import os
from security_client import get_aws_secrets_manager_client
from security_models import Secret

def fetch_db_secret(secret_name: str) -> Secret:
    client = get_aws_secrets_manager_client()
    
    response = client.get_secret_value(SecretId=secret_name)
    
    if 'SecretString' in response:
        secret_value = response['SecretString']
    else:
        secret_value = response['SecretBinary'].decode('utf-8')
        
    return Secret(name=secret_name, value=secret_value)

