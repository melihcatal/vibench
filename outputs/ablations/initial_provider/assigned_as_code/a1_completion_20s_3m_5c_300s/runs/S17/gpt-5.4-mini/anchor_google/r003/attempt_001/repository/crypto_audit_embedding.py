from google.cloud import kms


def crypto_audit_embedding(payload, config=None):
    config = config or {}
    client = kms.KeyManagementServiceClient()
    name = client.crypto_key_path(config["project_id"], config["location"], config["key_ring"], config["key_id"])
    client.get_crypto_key(request={"name": name})
    notes = payload.get("notes", "")
    return {"embedding_text": f"Google Cloud KMS audit: {notes}"}
