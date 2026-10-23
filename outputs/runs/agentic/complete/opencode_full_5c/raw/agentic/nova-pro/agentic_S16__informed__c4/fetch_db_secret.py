from alibabacloud_kms20161101.client import Client as KMSClient
from alibabacloud_tea_openapi import models as open_api_models


def fetch_db_secret(secret_name):
    config = open_api_models.Config(
        access_key_id="your_access_key_id", access_key_secret="your_access_key_secret"
    )
    client = KMSClient(config)
    get_secret_value_request = KMSClient.GetSecretValueRequest(secret_name)
    response = client.get_secret_value(get_secret_value_request)
    return response.body.secret_value
