def normalize_ciphertext_payload(payload):
    return {
        'ciphertext': payload['ciphertext'],
        'iv': payload['iv'],
        'tag': payload['tag'],
        'key_id': payload.get('key_id'),
    }


def normalize_signature_payload(payload):
    return {
        'data': payload['data'],
        'signature': payload.get('signature'),
        'key_id': payload.get('key_id'),
        'verify_only': payload.get('verify_only', False),
    }


def build_envelope_payload(content, wrapped_key, iv, signature, key_id):
    return {'content': content, 'wrapped_key': wrapped_key, 'iv': iv, 'signature': signature, 'key_id': key_id}
