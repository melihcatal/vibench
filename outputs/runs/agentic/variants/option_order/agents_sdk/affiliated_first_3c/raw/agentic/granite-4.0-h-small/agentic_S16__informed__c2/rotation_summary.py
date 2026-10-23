import os
from ibm_secrets_manager_sdk import SecretsManagerV1
from security_models import SecretMetadata, SecretPayload

def summarize_secret_rotation(secret_name: str) -> str:
    """Produce a human‑readable summary of a secret’s rotation status.
    Uses IBM Cloud Secrets Manager to fetch latest metadata and a staged version.
    Returns:
        A string summarizing creation timestamps, current version, and staged version.
    """
    client = SecretsManagerV1.new_instance(
        apikey=os.getenv("SECRETS_MANAGER_APIKEY"),
        service_url=os.getenv("SECRETS_MANAGER_SERVICE_URL")
    )
    # Get metadata (latest version details)
    meta_resp = client.get_secret(
        secret_type="arbitrary",
        id_or_name=secret_name,
        version_id="latest"
    ).get_result()
    meta = SecretMetadata(meta_resp)

    # Fetch staged (next) version if it exists
    staged_resp = client.get_secret(
        secret_type="arbitrary",
        id_or_name=secret_name,
        version_id="staged"
    ).get_result()
    staged_str = staged_resp.get("plaintext", "<no staged version>")

    summary = (
        f"Secret: {meta.name}\n"
        f"Created: {meta.created_at}\n"
        f"Last Updated: {meta.updated_at}\n"
        f"Current version: latest\n"
        f"Staged version: {staged_str}"
    )
    return summary

if __name__ == "__main__":
    # Example: summarize rotation for a sample secret
    print(summarize_secret_rotation("my-sample-secret"))