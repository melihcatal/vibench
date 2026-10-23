def normalize_payload(payload):
    return {
        'plaintext': payload['plaintext'].encode('utf-8'),
        'algorithm': payload['algorithm'].upper()
    }


def normalize_response(response):
    return {
        'ciphertext': response['ciphertext'].decode('utf-8'),
        'iv': response['iv'].decode('utf-8'),
        'tag': response['tag'].decode('utf-8'),
        'key_id': response['key_id'].decode('utf-8'),
        'algorithm': response['algorithm'].decode('utf-8')
    }