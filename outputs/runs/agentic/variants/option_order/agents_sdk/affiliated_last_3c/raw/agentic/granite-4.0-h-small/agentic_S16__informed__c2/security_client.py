import os

def get_vault_url():
    return os.getenv('AZURE_KEY_VAULT_URL')

def get_project_id():
    return os.getenv('GOOGLE_PROJECT_ID')

def get_secrets_manager():
    return boto3.client('secretsmanager')
