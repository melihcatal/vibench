class EncryptRequest:
    def __init__(self, payload):
        self.payload = payload


class DecryptRequest:
    def __init__(self, ciphertext):
        self.ciphertext = ciphertext


class EnvelopeEncryptRequest:
    def __init__(self, payload):
        self.payload = payload


class SignVerifyRequest:
    def __init__(self, payload, signature):
        self.payload = payload
        self.signature = signature
