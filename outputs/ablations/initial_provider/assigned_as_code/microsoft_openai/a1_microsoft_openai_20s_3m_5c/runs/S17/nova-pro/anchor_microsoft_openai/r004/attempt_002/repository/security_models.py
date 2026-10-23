def normalize_payload(payload):
    return {'plaintext': payload}

def normalize_ciphertext(ciphertext):
    return {'ciphertext': ciphertext['ciphertext'], 'iv': ciphertext['iv'], 'tag': ciphertext['tag']}

def normalize_envelope(envelope):
    return {'ciphertext': envelope['ciphertext'], 'iv': envelope['iv'], 'tag': envelope['tag']}