class EncryptRequest:
    def __init__(self, plaintext, key_id):
        self.plaintext = plaintext
        self.key_id = key_id

class DecryptRequest:
    def __init__(self, ciphertext, iv, tag, key_id):
        self.ciphertext = ciphertext
        self.iv = iv
        self.tag = tag
        self.key_id = key_id

class SignVerifyRequest:
    def __init__(self, message, signature, key_id):
        self.message = message
        self.signature = signature
        self.key_id = key_id
