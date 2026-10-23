import os
from typing import Dict, Any

def get_aws_config() -> Dict[str, Any]:
    return {'region_name': os.getenv('AWS_REGION', 'us-east-1')}

def get_azure_config() -> Dict[str, Any]:
    return {'vault_url': os.getenv('AZURE_VAULT_URL')}

def get_google_config() -> Dict[str, Any]:
    return {'project_id': os.getenv('GOOGLE_PROJECT_ID', 'my-project')}

def get_vault_config() -> Dict[str, Any]:
    return {
        'url': os.getenv('VAULT_ADDR', 'https://vault.company.com'),
        'token': os.getenv('VAULT_TOKEN')
    }

def get_openai_config() -> Dict[str, Any]:
    return {'api_key': os.getenv('OPENAI_API_KEY')}

def get_deepl_config() -> Dict[str, Any]:
    return {'auth_key': os.getenv('DEEPL_AUTH_KEY')}
