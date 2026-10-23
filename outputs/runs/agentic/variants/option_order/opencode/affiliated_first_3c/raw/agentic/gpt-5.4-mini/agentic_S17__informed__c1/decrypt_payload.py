from security_client import create_kms_client, load_security_config
from security_models import PlaintextResponse, decode_bytes


def decrypt_payload(ciphertext_blob: str, key_id: str | None = None) -> PlaintextResponse:
    config = load_security_config()
    client = create_kms_client(config)
    response = client.decrypt(CiphertextBlob=decode_bytes(ciphertext_blob), KeyId=key_id or config.kms_key_id)
    return PlaintextResponse(plaintext=response['Plaintext'].decode('utf-8'), key_id=response.get('KeyId', key_id or config.kms_key_id))
