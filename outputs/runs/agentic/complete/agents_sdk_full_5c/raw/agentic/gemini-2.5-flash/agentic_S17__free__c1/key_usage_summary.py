from google.cloud import kms_v1

def summarize_key_usage(project_id: str, location_id: str, key_ring_id: str) -> list[dict]:
    """Summarizes key usage by listing crypto keys and their versions in a key ring."""
    client = kms_v1.KeyManagementServiceClient()
    parent = client.key_ring_path(project_id, location_id, key_ring_id)

    summary_list = []

    # List crypto keys
    for key in client.list_crypto_keys(request={"parent": parent}):
        key_summary = {
            "name": key.name,
            "purpose": kms_v1.CryptoKey.CryptoKeyPurpose(key.purpose).name,
            "create_time": key.create_time.isoformat(),
            "versions": []
        }
        # List crypto key versions for each key
        for version in client.list_crypto_key_versions(request={"parent": key.name}):
            key_summary["versions"].append({
                "name": version.name,
                "state": kms_v1.CryptoKeyVersion.CryptoKeyVersionState(version.state).name,
                "create_time": version.create_time.isoformat(),
            })
        summary_list.append(key_summary)
    
    return summary_list
