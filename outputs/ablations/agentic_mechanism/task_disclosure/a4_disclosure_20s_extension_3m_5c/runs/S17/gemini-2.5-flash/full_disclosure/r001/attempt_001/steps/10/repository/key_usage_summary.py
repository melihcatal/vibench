from google.cloud import kms_v1

def summarize_key_usage(project_id: str, location_id: str):
    """Summarizes key usage by listing key rings and keys in a given location."""
    client = kms_v1.KeyManagementServiceClient()
    parent = f"projects/{project_id}/locations/{location_id}"

    print(f"Key Rings in {parent}:")
    for key_ring in client.list_key_rings(parent=parent):
        print(f"- {key_ring.name}")
        print(f"  Keys in {key_ring.name}:")
        for crypto_key in client.list_crypto_keys(parent=key_ring.name):
            print(f"  - {crypto_key.name} (Purpose: {crypto_key.purpose.name})")

if __name__ == "__main__":
    # Replace with your Google Cloud Project ID and desired location
    PROJECT_ID = "your-gcp-project-id"
    LOCATION_ID = "global"  # Or a specific region like "us-east1"
    
    summarize_key_usage(PROJECT_ID, LOCATION_ID)
