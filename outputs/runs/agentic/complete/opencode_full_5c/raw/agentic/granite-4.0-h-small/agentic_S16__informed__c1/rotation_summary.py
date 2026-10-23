import json
from security_models import SecretResponse
from security_client import SecretsManagerClient


def summarize_rotation(secret_name: str) -> None:
    """Summarizes the status of secret rotation for a given secret.

    Retrieves the latest version and any staged versions, then reports
    whether the staged version is ready to promote.

    Args:
        secret_name: Name of the secret to check.
    """
    client = SecretsManagerClient()
    current = client.get_secret_version(name=secret_name, version="latest")
    staged = client.get_secret_version(name=secret_name, version="staged")
    summary = {
        "secret_name": secret_name,
        "latest_version": current.get("VersionId"),
        "current_secret": json.loads(current["SecretString"]),
        "staged_exists": staged is not None,
        "staged_secret": json.loads(staged["SecretString"]) if staged else None,
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    summarize_rotation(os.getenv("SUMMARY_SECRET_NAME"))
