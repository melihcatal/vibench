def payload_request(plaintext=None, ciphertext=None, key_id=None, algorithm=None, iv=None, tag=None, aad=None):
    return {
        'plaintext': plaintext,
        'ciphertext': ciphertext,
        'key_id': key_id,
        'algorithm': algorithm,
        'iv': iv,
        'tag': tag,
        'aad': aad,
    }


def response_payload(**kwargs):
    data = {}
    for key, value in kwargs.items():
        if value is not None:
            data[key] = value
    return data


def normalize_crypto_payload(payload):
    payload = dict(payload or {})
    if 'plaintext' in payload and isinstance(payload['plaintext'], str):
        payload['plaintext'] = payload['plaintext'].encode('utf-8')
    if 'ciphertext' in payload and isinstance(payload['ciphertext'], str):
        payload['ciphertext'] = payload['ciphertext'].encode('utf-8')
    return payload
