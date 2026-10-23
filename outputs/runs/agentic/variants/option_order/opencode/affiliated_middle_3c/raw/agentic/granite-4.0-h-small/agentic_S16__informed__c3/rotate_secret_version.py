import boto3

secret_client = boto3.client(
    "secretsmanager",
    # credentials are set via AWS environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, optional AWS_REGION)
)


def rotate_secret_version(secret_id: str, version_stage: str = "AWSCURRENT") -> dict:
    """Read a particular version of a secret using version stage identifiers.

    Args:
        secret_id: Identifier of the secret.
        version_stage: Stage label (e.g., 'AWSCURRENT', 'AWSPREVIOUS').

    Returns:
        Response dictionary from Secrets Manager containing the secret payload.
    """
    return secret_client.get_secret_value(
        SecretId=secret_id, VersionStage=version_stage
    )
