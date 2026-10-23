from ibm_secrets_manager_sdk import SecretsManagerV2


def rotate_secret_version(apikey, instance_id, secret_id, version_id):
    service = SecretsManagerV2(
        iam_apikey=apikey,
        service_url="https://us-south.secrets-manager.appdomain.cloud",
    )
    response = service.get_secret_version(
        instance_id=instance_id, secret_id=secret_id, version_custom_metadata=version_id
    ).get_result()
    return response
