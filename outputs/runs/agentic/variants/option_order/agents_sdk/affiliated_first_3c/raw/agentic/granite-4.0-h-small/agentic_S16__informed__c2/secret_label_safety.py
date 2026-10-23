import os
from ibm_secrets_manager_sdk import SecretsManagerV1
from security_models import parse_secret_response
from typing import Any, Dict

def check_secret_labels(secret_name: str) -> None:
    """Validate that secret labels/notes do not contain unsafe text.
    Uses a simple heuristic: reject any label containing the word 'unsafe'.
    Raises:
        ValueError if an unsafe label is detected.
    """
    client = SecretsManagerV1.new_instance(
        apikey=os.getenv("SECRETS_MANAGER_APIKEY"),
        service_url=os.getenv("SECRETS_MANAGER_SERVICE_URL")
    )
    resp = client.get_secret(
        secret_type="arbitrary",
        id_or_name=secret_name,
        version_id="latest"
    ).get_result()
    meta, _ = parse_secret_response(resp)
    unsafe = [lbl for lbl in meta.labels if "unsafe" in lbl.lower()]
    if unsafe:
        raise ValueError(f"Unsafe label(s) found: {unsafe}")
    print(f"Labels for '{secret_name}' are safe.")

if __name__ == "__main__":
    # Example usage – replace with an actual secret name
    check_secret_labels("my-test-secret")