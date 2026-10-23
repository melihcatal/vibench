import os
from security_client import get_secrets_manager_client

def get_secret_version(secret_id: str, version_id: str = None, version_stage: str = None) -> str:
    client = get_secrets_manager_client()
    retrieve_params = {"SecretId": secret_id}
    if version_id:
        retrieve_params["VersionId"] = version_id
    if version_stage:
        retrieve_params["VersionStage"] = version_stage
    
    try:
        get_secret_value_response = client.get_secret_value(**retrieve_params)
        if 'SecretString' in get_secret_value_response:
            return get_secret_value_response['SecretString']
        elif 'SecretBinary' in get_secret_value_response:
            return get_secret_value_response['SecretBinary'].decode('utf-8')
    except client.exceptions.ResourceNotFoundException:
        raise
    except Exception:
        raise
    return ""
