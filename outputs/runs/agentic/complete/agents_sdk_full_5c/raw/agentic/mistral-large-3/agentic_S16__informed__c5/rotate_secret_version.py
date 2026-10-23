from alibabacloud_kms20160120.client import Client as Kms20160120Client
from alibabacloud_tea_openapi import models as openapi_models
from alibabacloud_kms20160120 import models as kms_models


def rotate_secret_version(
    access_key_id: str, 
    access_key_secret: str, 
    region_id: str, 
    secret_name: str, 
    version_stage: str = "ACSCurrent"
) -> str:
    """
    Reads a specific secret version or staged value from Alibaba KMS Secrets Manager.
    
    Args:
        access_key_id: Alibaba Cloud access key ID.
        access_key_secret: Alibaba Cloud access key secret.
        region_id: The region where the secret is stored.
        secret_name: The name of the secret to fetch.
        version_stage: The version stage to fetch (default: "ACSCurrent").
        
    Returns:
        The secret value as a string.
    """
    config = openapi_models.Config(
        access_key_id=access_key_id,
        access_key_secret=access_key_secret,
        region_id=region_id
    )
    client = Kms20160120Client(config)
    request = kms_models.GetSecretValueRequest(
        secret_name=secret_name,
        version_stage=version_stage
    )
    response = client.get_secret_value(request)
    return response.secret_data