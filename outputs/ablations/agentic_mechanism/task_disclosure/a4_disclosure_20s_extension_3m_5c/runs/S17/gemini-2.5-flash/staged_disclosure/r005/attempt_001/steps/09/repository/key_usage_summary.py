import os
from google.cloud import kms

def summarize_key_usage(project_id: str, location_id: str):
    """Summarizes key usage and crypto events for a given project and location."""
    
    client = kms.KeyManagementServiceClient()
    location_path = client.common_location_path(project_id, location_id)

    print(f"Key Usage Summary for Project: {project_id}, Location: {location_id}\n")

    # List key rings
    for key_ring in client.list_key_rings(parent=location_path):
        print(f"Key Ring: {key_ring.name}")

        # List crypto keys within each key ring
        for crypto_key in client.list_crypto_keys(parent=key_ring.name):
            print(f"  Crypto Key: {crypto_key.name}")
            print(f"    Purpose: {crypto_key.purpose.name}")
            print(f"    Create Time: {crypto_key.create_time}")
            # In a real scenario, you would integrate with Cloud Logging or other services
            # to fetch actual crypto events related to this key.
            print("    (Placeholder for crypto event summary - integrate with Cloud Logging for details)")
        print("-" * 20)

if __name__ == "__main__":
    # Replace with your Google Cloud Project ID and desired location
    PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT_ID", "your-gcp-project-id")
    LOCATION_ID = os.environ.get("GOOGLE_CLOUD_LOCATION_ID", "global") 

    if PROJECT_ID == "your-gcp-project-id":
        print("Please set the GOOGLE_CLOUD_PROJECT_ID environment variable or replace 'your-gcp-project-id' in the script.")
    else:
        summarize_key_usage(PROJECT_ID, LOCATION_ID)
