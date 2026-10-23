import os
from typing import Dict, Any

def get_secrets_config() -> Dict[str, Any]:
    return {
        'aws_region': os.getenv('AWS_REGION', 'us-east-1'),
        'gcp_project_id': os.getenv('GCP_PROJECT_ID', 'my-project'),
        'azure_vault_url': os.getenv('AZURE_VAULT_URL', 'https://mykeyvault.vault.azure.net'),
        'vault_addr': os.getenv('VAULT_ADDR', 'https://vault.company.com:8200'),
        'openai_api_key': os.getenv('OPENAI_API_KEY'),
        'perspective_api_key': os.getenv('PERSPECTIVE_API_KEY'),
        'deepl_api_key': os.getenv('DEEPL_API_KEY'),
    }