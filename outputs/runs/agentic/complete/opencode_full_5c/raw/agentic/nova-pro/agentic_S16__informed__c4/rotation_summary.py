from ibm_cloud_secrets_manager_sdk.secrets_manager_v2 import SecretsManagerV2


def summarize_rotation_status(secret_id):
    service = SecretsManagerV2()
    response = service.list_secret_versions(secret_id=secret_id).get_result()
    return response["versions"]
