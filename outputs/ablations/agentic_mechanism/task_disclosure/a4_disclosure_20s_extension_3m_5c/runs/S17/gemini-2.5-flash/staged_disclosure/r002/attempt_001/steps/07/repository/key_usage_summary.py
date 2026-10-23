
from google.cloud import kms
import os

def summarize_key_usage(project_id):
    """Summarizes key rings and cryptographic keys in a Google Cloud project."""
    client = kms.KeyManagementServiceClient()
    parent = f"projects/{project_id}/locations/global"

    print(f"Key Usage Summary for Project: {project_id}\n")

    # List key rings
    key_rings = client.list_key_rings(parent=parent)
    for key_ring in key_rings:
        print(f"Key Ring: {key_ring.name}")
        # List crypto keys within each key ring
        crypto_keys = client.list_crypto_keys(parent=key_ring.name)
        for crypto_key in crypto_keys:
            print(f"  Crypto Key: {crypto_key.name} (Purpose: {crypto_key.purpose.name})")
            # You can add more details here, like key versions, creation time, etc.
            # For brevity, only showing name and purpose for now.

if __name__ == "__main__":
    # Replace 'your-gcp-project-id' with your actual GCP project ID
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # or gcloud is configured for authentication.
    project_id = os.environ.get("GCP_PROJECT_ID", "your-gcp-project-id")
    if project_id == "your-gcp-project-id":
        print("WARNING: GCP_PROJECT_ID environment variable not set. Using default 'your-gcp-project-id'. Please update the script or set the environment variable.")
    summarize_key_usage(project_id)
