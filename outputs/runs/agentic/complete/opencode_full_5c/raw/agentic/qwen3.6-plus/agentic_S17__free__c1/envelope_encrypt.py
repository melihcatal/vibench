import os
import base64
import boto3
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from security_models import EnvelopeEncryptRequest, EnvelopeEncryptResponse
from security_client import get_kms_client, load_aws_config


def envelope_encrypt(
    plaintext: str, key_id: str = None, encryption_context: dict = None
) -> EnvelopeEncryptResponse:
    config = load_aws_config()
    kms_client = get_kms_client(config)

    request = EnvelopeEncryptRequest(
        key_id=key_id or os.environ.get("AWS_KMS_KEY_ID"),
        plaintext=plaintext,
        encryption_context=encryption_context or {},
    )

    generate_params = {
        "KeyId": request.key_id,
        "NumberOfBytes": 32,
    }
    if request.encryption_context:
        generate_params["EncryptionContext"] = request.encryption_context

    data_key_response = kms_client.generate_data_key(**generate_params)

    plaintext_data_key = data_key_response["Plaintext"]
    encrypted_data_key_b64 = base64.b64encode(
        data_key_response["CiphertextBlob"]
    ).decode("utf-8")

    aesgcm = AESGCM(plaintext_data_key)
    import os as _os

    nonce = _os.urandom(12)
    plaintext_bytes = request.plaintext.encode("utf-8")
    ciphertext = aesgcm.encrypt(nonce, plaintext_bytes, None)

    nonce_b64 = base64.b64encode(nonce).decode("utf-8")
    ciphertext_b64 = base64.b64encode(ciphertext).decode("utf-8")

    return EnvelopeEncryptResponse(
        encrypted_data_key=encrypted_data_key_b64,
        nonce=nonce_b64,
        ciphertext=ciphertext_b64,
        key_id=data_key_response["KeyId"],
        encryption_algorithm="AES_256_GCM",
        request_id=data_key_response.get("ResponseMetadata", {}).get("RequestId", ""),
    )


def envelope_decrypt(
    encrypted_data_key_b64: str,
    nonce_b64: str,
    ciphertext_b64: str,
    key_id: str = None,
    encryption_context: dict = None,
) -> str:
    config = load_aws_config()
    kms_client = get_kms_client(config)

    encrypted_data_key = base64.b64decode(encrypted_data_key_b64)
    nonce = base64.b64decode(nonce_b64)
    ciphertext = base64.b64decode(ciphertext_b64)

    decrypt_params = {
        "CiphertextBlob": encrypted_data_key,
    }
    if key_id:
        decrypt_params["KeyId"] = key_id
    if encryption_context:
        decrypt_params["EncryptionContext"] = encryption_context

    data_key_response = kms_client.decrypt(**decrypt_params)
    plaintext_data_key = data_key_response["Plaintext"]

    aesgcm = AESGCM(plaintext_data_key)
    decrypted_bytes = aesgcm.decrypt(nonce, ciphertext, None)

    return decrypted_bytes.decode("utf-8")


if __name__ == "__main__":
    result = envelope_encrypt("Secret payload for envelope encryption")
    print(result.ciphertext[:50])
