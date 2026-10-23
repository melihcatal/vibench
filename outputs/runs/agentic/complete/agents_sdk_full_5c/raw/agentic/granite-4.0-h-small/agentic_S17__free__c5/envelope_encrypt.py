import os
import json
from security_client import KmsClient
from security_models import EncryptRequest, EncryptResponse, DecryptRequest, DecryptResponse

# Use AWS KMS as the concrete managed key service
# The client loads AWS credentials from environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)

def envelope_encrypt(plaintext: str) -> dict:
    """Performs envelope encryption:
    1. Generates a data key via KMS GenerateDataKey.
    2. Encrypts plaintext with the plaintext data key (AES‑256‑GCM).
    3. Encrypts the data key itself with the managed KMS key (ciphertext_blob).
    Returns a dict containing both ciphertext_blob and encrypted_data.
    """
    client = KmsClient()
    # 1. Generate a data key (plaintext + ciphertext_blob) from KMS
    gen_resp = client.generate_data_key(KeyId='alias/MyKMSEncryptionKey', KeySpec='AES_256')
    data_key_plaintext = gen_resp['Plaintext']
    data_key_ciphertext = gen_resp['CiphertextBlob']
    # 2. Encrypt plaintext locally with the plaintext data key (simple AES example)
    from Crypto.Cipher import AES
    from Crypto.Random import get_random_bytes
    from Crypto.Util.Padding import pad
    iv = get_random_bytes(12)  # GCM IV
    cipher = AES.new(data_key_plaintext, AES.MODE_GCM, iv)
    ciphertext, tag = cipher.encrypt_and_digest(pad(plaintext.encode('utf-8'), AES.block_size))
    # Package result
    return {
        'ciphertext': ciphertext,
        'iv': iv,
        'tag': tag,
        'encrypted_data_key': data_key_ciphertext.decode('utf-8')
    }

if __name__ == "__main__":
    pt = "Sensitive data that must stay encrypted at rest."
    envelope = envelope_encrypt(pt)
    print(json.dumps({
        'ciphertext_base64': envelope['ciphertext'].decode('latin1'),
        'iv_base64': envelope['iv'].hex(),
        'tag_base64': envelope['tag'].hex(),
        'encrypted_data_key_base64': envelope['encrypted_data_key']
    }, ensure_ascii=False))
