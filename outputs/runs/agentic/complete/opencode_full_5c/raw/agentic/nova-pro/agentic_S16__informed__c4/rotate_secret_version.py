from ibm_cloud_secrets_manager_sdk.secrets_manager_v2 import SecretsManagerV2


def rotate_secret_version(secret_id, version_id):
    service = SecretsManagerV2()
    response = service.get_secret_version(
        secret_id=secret_id, version_id=version_id
    ).get_result()
    return response["secret_data"]
