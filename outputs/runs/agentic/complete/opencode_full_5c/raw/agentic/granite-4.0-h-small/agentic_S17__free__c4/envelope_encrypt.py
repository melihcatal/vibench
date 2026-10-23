import base64, json
from security_client import get_key_management_client

# Google Cloud KMS envelope encryption example


def envelope_encrypt(plaintext: str, data_key_id: str, encryption_key_id: str) -> dict:
    """Perform envelope encryption: encrypt data with a data key,
    then encrypt the data key with a managed key.

    Returns a dict with the encrypted data and the wrapped (encrypted)
    data key.
    """
    client = get_key_management_client()
    # 1. Generate a random data encryption key (DER) – could be replaced with
    #    a real service call if the provider offers key generation.
    data_key = os.urandom(32)  # 256‑bit AES key
    # 2. Encrypt the plaintext with the data key (AES‑GCM example)
    from Crypto.Cipher import AES
    from Crypto.Random import get_random_bytes

    iv = get_random_bytes(12)
    cipher = AES.new(data_key, AES.MODE_GCM, iv)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext.encode("utf-8"))
    encrypted_data = {
        "iv": base64.b64encode(iv).decode(),
        "ciphertext": base64.b64encode(ciphertext).decode(),
        "tag": base64.b64encode(tag).decode(),
    }
    # 3. Encrypt the data key with the managed envelope key
    response = client.encrypt(KeyId=encryption_key_id, Plaintext=data_key)
    wrapped_key = base64.b64encode(response["CiphertextBlob"]).decode()
    return {"encrypted_data": encrypted_data, "wrapped_key": wrapped_key}
