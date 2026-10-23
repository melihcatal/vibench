import os

import boto3
from Crypto.Cipher import AES

from security_client import load_security_client_config
from security_models import EnvelopeEncryptResponse, b64encode_bytes, normalize_text


def envelope_encrypt(plaintext: str) -> EnvelopeEncryptResponse:
    config = load_security_client_config()
    kms = boto3.client("kms", region_name=config.region_name)
    data_key = kms.generate_data_key(KeyId=config.kms_key_id, KeySpec="AES_256")
    raw_key = data_key["Plaintext"]
    iv = os.urandom(12)
    cipher = AES.new(raw_key, AES.MODE_GCM, nonce=iv)
    ciphertext, tag = cipher.encrypt_and_digest(normalize_text(plaintext).encode("utf-8"))
    return EnvelopeEncryptResponse(
        encrypted_data_key=b64encode_bytes(data_key["CiphertextBlob"]),
        iv=b64encode_bytes(iv),
        ciphertext=b64encode_bytes(ciphertext + tag),
        key_id=data_key["KeyId"],
    )


def main() -> None:
    envelope_encrypt("sample plaintext")


if __name__ == "__main__":
    main()
