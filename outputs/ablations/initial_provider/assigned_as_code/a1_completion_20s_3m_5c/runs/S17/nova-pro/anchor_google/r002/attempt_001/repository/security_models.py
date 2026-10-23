def normalize_response(response):
    return {"ciphertext": response.ciphertext}


def normalize_payload(payload):
    return {"plaintext": payload}