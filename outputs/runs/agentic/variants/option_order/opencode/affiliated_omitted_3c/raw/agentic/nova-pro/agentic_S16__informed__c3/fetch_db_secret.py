from alibabacloud_kms20160120.client import Client as KMSClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_kms20160120 import models as kms_models


def fetch_db_secret(config, secret_name):
    config = open_api_models.Config(
        access_key_id=config.access_key_id, access_key_secret=config.access_key_secret
    )
    client = KMSClient(config)
    request = kms_models.GetSecretValueRequest(secret_name=secret_name)
    response = client.get_secret_value(request)
    return response.body.secret_value
