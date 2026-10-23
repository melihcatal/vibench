import os
import json

class SecretsClient:
    """Centralized Secrets Manager client using IBM Cloud Secrets Manager SDK."""
    _APIKEY = os.getenv("IBM_SECRETS_MANAGER_APIKEY")
    if not _APIKEY:
        raise RuntimeError("Set IBM_SECRETS_MANAGER_APIKEY environment variable")

    _service = None
    def _get_service(self):
        if self._service is None:
            from ibm_secrets_manager_sdk import SecretsManagerV1
            from ibm_secrets_manager_sdk.integrations.client_factory import ClientFactory
            self._service = ClientFactory.create_service(SecretsManagerV1, "secrets-manager", endpoint="https://us-south.secrets-manager.appdomain.cloud")
            self._service.set_apikey(self._APIKEY)
        return self._service

    def get_secret(self, secret_id: str, version_id: str = "latest") -> dict:
        """Retrieve a secret and return the parsed JSON payload."""
        resp = self._get_service().get_secret_version(secret_id=secret_id, version_id=version_id)
        payload = resp.get_result().get_result()
        import json
        return json.loads(payload)
