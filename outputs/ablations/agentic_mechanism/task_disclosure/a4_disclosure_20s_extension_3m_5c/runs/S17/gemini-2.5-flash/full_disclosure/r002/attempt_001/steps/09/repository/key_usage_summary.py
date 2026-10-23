from google.cloud import kms_v1

def summarize_key_usage(project_id: str, location_id: str):
    """Summarizes key usage and crypto events by listing keys and their properties."""
    client = kms_v1.KeyManagementServiceClient()
    location_path = client.common_location_path(project_id, location_id)

    print(f"Summarizing key usage in project {project_id}, location {location_id}:")

    for key_ring in client.list_key_rings(parent=location_path):
        print(f"  Key Ring: {key_ring.name.split('/')[-1]}")
        for crypto_key in client.list_crypto_keys(parent=key_ring.name):
            print(f"    Crypto Key: {crypto_key.name.split('/')[-1]}")
            print(f"      Purpose: {kms_v1.CryptoKey.CryptoKeyPurpose(crypto_key.purpose).name}")
            print(f"      Create Time: {crypto_key.create_time.isoformat()}")

if __name__ == "__main__":
    # This is placeholder for demonstration and would typically be configured via environment variables or a config file.
    # Replace with your actual Google Cloud project ID and desired location.
    # project_id = "your-gcp-project-id"
    # location_id = "global"  # or "us-central1", etc.
    # summarize_key_usage(project_id, location_id)
    pass
