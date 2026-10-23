from security_client import decrypt_with_kms, load_config
from security_models import DecryptPayloadRequest, response_map


def decrypt_payload(key_id: str, ciphertext):
    request = DecryptPayloadRequest(key_id=key_id, ciphertext=ciphertext)
    plaintext = decrypt_with_kms(request.key_id, request.ciphertext)
    return response_map(key_id=request.key_id, plaintext=plaintext)


if __name__ == '__main__':
    config = load_config()
    print(decrypt_payload(config['kms_key_id'], ''))
