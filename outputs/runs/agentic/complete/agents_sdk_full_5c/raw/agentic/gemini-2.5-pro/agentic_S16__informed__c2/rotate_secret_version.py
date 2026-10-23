from security_client import get_secrets_manager_client

def read_secret_by_stage(secret_name: str, stage: str = "AWSCURRENT") -> str:
    """
    Reads a specific version of a secret identified by its stage label.
    In AWS Secrets Manager, common stages are AWSCURRENT, AWSPENDING, AWSPREVIOUS.

    Args:
        secret_name: The name or ARN of the secret.
        stage: The staging label of the version to retrieve.

    Returns:
        The secret string for the specified stage.
    """
    client = get_secrets_manager_client()
    
    response = client.get_secret_value(
        SecretId=secret_name,
        VersionStage=stage
    )
    
    return response['SecretString']
