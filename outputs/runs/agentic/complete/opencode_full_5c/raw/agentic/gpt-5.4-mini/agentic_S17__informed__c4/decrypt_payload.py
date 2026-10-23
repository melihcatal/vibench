from security_client import decode_bytes, kms_client, load_config


def decrypt_payload(ciphertext: str, key_id: str | None = None) -> dict:
    config = load_config()
    client = kms_client(config)
    response = client.decrypt(
        CiphertextBlob=decode_bytes(ciphertext), KeyId=key_id or config.key_id
    )
    return {
        "key_id": key_id or config.key_id,
        "plaintext": response["Plaintext"].decode("utf-8"),
    }
