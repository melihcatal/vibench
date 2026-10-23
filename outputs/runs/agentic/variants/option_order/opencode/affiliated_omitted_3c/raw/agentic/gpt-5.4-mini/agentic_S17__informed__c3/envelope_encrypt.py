import base64
import os

from security_client import get_config, get_kms_client
from security_models import EncryptionEnvelope, normalize_text


def envelope_encrypt(plaintext: str, key_id: str | None = None) -> EncryptionEnvelope:
    cfg = get_config()
    client = get_kms_client()
    resolved_key_id = key_id or cfg["default_key_id"]
    data_key = client.generate_data_key(KeyId=resolved_key_id, KeySpec="AES_256")
    dek_plaintext = data_key["Plaintext"]
    dek_encrypted = base64.b64encode(data_key["CiphertextBlob"]).decode("ascii")
    nonce = os.urandom(12)
    payload = normalize_text(plaintext).encode("utf-8")
    ciphertext = base64.b64encode(nonce + payload).decode("ascii")
    return EncryptionEnvelope(
        encrypted_data_key=dek_encrypted,
        ciphertext=ciphertext,
        key_id=resolved_key_id,
        provider=cfg["provider"],
    )
