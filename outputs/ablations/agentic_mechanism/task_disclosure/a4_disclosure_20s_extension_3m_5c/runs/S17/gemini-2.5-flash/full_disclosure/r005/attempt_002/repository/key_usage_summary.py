from google.cloud import kms

def summarize_key_usage(project_id, location_id):
    """Summarizes key usage by listing key rings and keys in a given location."""
    client = kms.KeyManagementServiceClient()
    location_path = f"projects/{project_id}/locations/{location_id}"

    key_rings = client.list_key_rings(parent=location_path)
    print(f"Key Rings in {location_path}:")
    for key_ring in key_rings:
        print(f"- {key_ring.name}")
        keys = client.list_crypto_keys(parent=key_ring.name)
        for key in keys:
            print(f"  - {key.name} (Purpose: {kms.CryptoKey.CryptoKeyPurpose(key.purpose).name})")

if __name__ == "__main__":
    # Replace with your Google Cloud project ID and location
    project_id = "your-gcp-project-id"
    location_id = "global"  # Or a specific region like "us-central1"
    summarize_key_usage(project_id, location_id)
