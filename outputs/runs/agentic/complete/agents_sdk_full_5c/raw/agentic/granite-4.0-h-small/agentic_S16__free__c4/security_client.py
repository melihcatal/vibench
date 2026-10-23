# security_client.py
# [HELPER]
# Local configuration and client helper utilities for Secret Management
import os
from typing import Any, Dict

# Provider-specific environment variables that guide client construction
def get_provider_env() -> Dict[str, str]:
    env = {
        'aws_role_arn': os.getenv('AWS_ROLE_ARN'),
        'aws_region': os.getenv('AWS_REGION', 'us-east-1'),
        'azure_tenant_id': os.getenv('AZURE_TENANT_ID'),
        'azure_client_id': os.getenv('AZURE_CLIENT_ID'),
        'azure_client_secret': os.getenv('AZURE_CLIENT_SECRET'),
        'azure_keyvault_name': os.getenv('AZURE_KEYVAULT_NAME'),
        'gcp_project_id': os.getenv('GCP_PROJECT_ID'),
        'gcp_secret_manager_location': os.getenv('GCP_SECRET_LOCATION', 'global'),
    }
    # Filter out empty values
    return {k: v for k, v in env.items() if v}

# Concrete client factories

def get_secret_manager_client() -> Any:
    """Return a boto3 Secrets Manager client with assumed role if configured.""",
    import boto3
    env = get_provider_env()
    if env.get('aws_role_arn'):
        # Assume the role and create a client
        sts_client = boto3.client('sts')
        assumed = sts_client.assume_role(RoleArn=env['aws_role_arn'], RoleSessionName='secret-client')
        credentials = assumed['Credentials']
        return boto3.client(
            'secretsmanager', 
            region_name=env['aws_region'], 
            aws_access_key_id=credentials['AccessKeyId'],
            aws_secret_access_key=credentials['SecretAccessKey'],
            aws_session_token=credentials['SessionToken']
        )
    # Fallback to default credentials chain
    return boto3.client('secretsmanager', region_name=env['aws_region'])

def get_vault_client() -> Any:
    """Create a HashiCorp Vault client using environment variables.""",
    import hvac
    token = os.getenv('VAULT_TOKEN')
    address = os.getenv('VAULT_ADDR', 'http://127.0.0.1:8200')
    client = hvac.Client(url=address)
    if token:
        client.auth.token_renewable.login(token=token)
    return client

def get_secret_value_response(client, secret_name: str, version: Any = 'latest') -> Dict[str, Any]:
    """Thin wrapper that dispatches to the underlying provider's get method.""",
    if hasattr(client, 'get_secret_value'):
        # AWS Secrets Manager
        return client.get_secret_value(SecretId=secret_name)
    elif hasattr(client, 'read_secret_version'):
        # GCP Secret Manager
        # For simplicity assume version is a string like 'latest'
        return client.access_secret_version(name=f'projects/-/secrets/{secret_name}/versions/{version}')
    raise ValueError('Unsupported client type')

# Logger placeholder (can be replaced with a real logger)
try:
    import logging
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
except Exception:
    logger = {'info': print, 'warning': print, 'error': print}

logger.info('Security client configured with env: %s', get_provider_env())
