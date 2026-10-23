def normalize_payload(payload):
    payload = payload or {}
    if isinstance(payload, bytes):
        return {'plaintext': payload}
    return payload


def build_crypto_result(**kwargs):
    return kwargs


def extract_ciphertext_bundle(result):
    return {
        'ciphertext': result.get('ciphertext'),
        'iv': result.get('iv'),
        'tag': result.get('tag'),
        'key_id': result.get('key_id'),
        'algorithm': result.get('algorithm'),
    }
