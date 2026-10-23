from security_client import create_kms_client, load_security_config
from security_models import PayloadRequest, CiphertextResponse, encode_bytes


def encrypt_payload(plaintext: str, key_id: str | None = None) -> CiphertextResponse:
    config = load_security_config()
    client = create_kms_client(config)
    request = PayloadRequest(plaintext=plaintext, key_id=key_id or config.kms_key_id)
    response = client.encrypt(KeyId=request.key_id, Plaintext=request.plaintext.encode('utf-8'))
    return CiphertextResponse(ciphertext_blob=encode_bytes(response['CiphertextBlob']), key_id=request.key_id)
