from google.cloud import kms
from google.cloud import storage

from security_client import build_kms_client, load_security_config


def envelope_encrypt(payload, config=None):
    config = load_security_config(config)
    kms_client = build_kms_client()
    storage_client = storage.Client()
    name = kms_client.crypto_key_path(config["project_id"], config["location"], config["key_ring"], config["key_id"])
    dek = payload["data_encryption_key"]
    wrapped_dek = kms_client.encrypt(request={"name": name, "plaintext": dek}).ciphertext
    bucket = storage_client.bucket(config["bucket"])
    blob = bucket.blob(payload["object_name"])
    blob.upload_from_string(payload["plaintext"])
    return {"wrapped_dek": wrapped_dek, "object_name": payload["object_name"]}
