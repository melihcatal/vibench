from security_client import get_secrets_client


def read_secret_version(
    secret_name: str, version_id: str = None, version_stage: str = "AWSPENDING"
) -> str:
    client = get_secrets_client()
    kwargs = {"SecretId": secret_name}
    if version_id:
        kwargs["VersionId"] = version_id
    if version_stage:
        kwargs["VersionStage"] = version_stage
    response = client.get_secret_value(**kwargs)
    return response["SecretString"]
