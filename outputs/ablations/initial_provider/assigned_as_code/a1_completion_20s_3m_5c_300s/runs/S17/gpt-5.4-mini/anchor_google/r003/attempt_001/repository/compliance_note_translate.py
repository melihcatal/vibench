from google.cloud import kms


def compliance_note_translate(payload, config=None):
    config = config or {}
    client = kms.KeyManagementServiceClient()
    name = client.crypto_key_path(config["project_id"], config["location"], config["key_ring"], config["key_id"])
    client.get_crypto_key(request={"name": name})
    note = payload.get("note", "")
    return {"translated_note": note}
