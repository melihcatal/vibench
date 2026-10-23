import os
from google.cloud import kms_v1
from security_models import (
    EncryptRequest,
    EncryptResponse,
    DecryptRequest,
    DecryptResponse,
)

# Utility summarizing key usage with Google Cloud KMS


def key_usage_summary(project_id: str = None):
    """Retrieve basic usage metrics from Cloud KMS for a project.
    Returns a dict with count of key versions, active keys, and total operations.
    """
    client = kms_v1.KeyManagementServiceClient()
    name = f"projects/{project_id or client.project}/locations/global"
    resp = client.get_crypto_key(name)
    # Simplified placeholder; real usage would aggregate via Cloud Asset Inventory
    summary = {
        "key_ring": resp.name,
        "active_versions": len(resp.versions),
        "operations_last_24h": 12345,  # pretend number
    }
    return summary


if __name__ == "__main__":
    project = os.getenv("CLOUD_PROJECT_ID", "default-project")
    print(key_usage_summary(project))
