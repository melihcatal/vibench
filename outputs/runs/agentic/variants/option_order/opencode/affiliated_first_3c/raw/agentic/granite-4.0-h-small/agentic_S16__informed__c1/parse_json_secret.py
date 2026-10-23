import os
import json
from ibm_secrets_manager_sdk import SecretsManagerV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator(os.getenv("IBM_SECRETS_MANAGER_APIKEY"))
secrets_manager = SecretsManagerV1.new_instance(
    service_url=os.getenv("IBM_SECRETS_MANAGER_URL"), authenticator=authenticator
)


def parse_json_secret(secret_name: str) -> dict:
    """Retrieve and parse a JSON-formatted secret stored in IBM Cloud Secrets Manager.
    Returns the parsed JSON object.
    """
    response = secrets_manager.get_secret(
        secret_id=secret_name, secret_type="arbitrary"
    )
    secret_data = response.get_result()
    secret_payload = secret_data["resources"][0]["secret_data"]["text"]
    return json.loads(secret_payload)


# Example usage
if __name__ == "__main__":
    json_secret = parse_json_secret("my-json-secret")
    print("Parsed JSON secret:", json_secret)
