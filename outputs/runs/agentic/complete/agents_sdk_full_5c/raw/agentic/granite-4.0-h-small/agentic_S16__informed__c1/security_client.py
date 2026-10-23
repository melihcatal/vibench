import os

class SecurityClient:
    """Local helper class that abstracts selection of a secret management backend.
    Currently supports IBM Cloud Secrets Manager via its SDK.
    """
    def __init__(self):
        self.api_key = os.getenv('IBM_SECRETS_MANAGER_APIKEY')
        if not self.api_key:
            raise RuntimeError('IBM_SECRETS_MANAGER_APIKEY not configured')
        from ibm_secrets_manager_sdk import SecretsManagerV1
        self.client = SecretsManagerV1.new_instance(api_key=self.api_key)

    def get_secret(self, secret_id):
        """Retrieve a secret's latest payload.
        Args:
            secret_id (str): Secret identifier.
        Returns:
            dict: Parsed JSON payload.
        """
        resp = self.client.get_secret(secret_id=secret_id)
        data = resp.get_result()
        import json
        return json.loads(data.get('secret_data', '{}'))

    def get_secret_version(self, secret_id, version):
        """Retrieve a specific version of a secret.
        Args:
            secret_id (str): Secret identifier.
            version (str): Version identifier (e.g., number or 'staged').
        Returns:
            dict: Parsed JSON payload of that version.
        """
        resp = self.client.get_secret(secret_id=secret_id, version=version)
        data = resp.get_result()
        import json
        return json.loads(data.get('secret_data', '{}'))
