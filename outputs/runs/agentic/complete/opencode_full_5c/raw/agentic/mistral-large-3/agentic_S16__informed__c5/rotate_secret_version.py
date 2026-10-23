from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_secrets_manager_sdk import SecretsManagerV2
import os


class IBMSecretsManagerClient:
    def __init__(self):
        authenticator = IAMAuthenticator(os.getenv("IBM_SECRETS_MANAGER_APIKEY"))
        self.client = SecretsManagerV2(authenticator=authenticator)
        self.client.set_service_url(os.getenv("IBM_SECRETS_MANAGER_URL"))

    def rotate_secret_version(self, secret_id: str, version_id: str = None) -> str:
        secret = self.client.get_secret(
            secret_type="arbitrary", id=secret_id
        ).get_result()

        if version_id:
            return next(
                (
                    v["secret_data"]
                    for v in secret["versions"]
                    if v["version_id"] == version_id
                ),
                None,
            )
        return secret["secret_data"]
