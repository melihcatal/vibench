import boto3


def rotate_secret_version(payload, config=None):
    config = config or {}
    client = boto3.client("secretsmanager", region_name=config.get("region"))
    
    # Parameters for get_secret_value
    params = {"SecretId": payload["secret_id"]}
    if payload.get("version_id"):
        params["VersionId"] = payload["version_id"]
    if payload.get("version_stage"):
        params["VersionStage"] = payload["version_stage"]
        
    response = client.get_secret_value(**params)
    value = response["SecretString"] if "SecretString" in response else response["SecretBinary"].decode("utf-8")
    
    return {
        "secret_value": value,
        "version_id": response.get("VersionId"),
        "version_stages": response.get("VersionStages"),
    }
