class EncryptRequest:
    def __init__(self, plaintext, key_id):
        self.plaintext = plaintext
        self.key_id = key_id


class DecryptRequest:
    def __init__(self, ciphertext, key_id):
        self.ciphertext = ciphertext
        self.key_id = key_id


class EnvelopeEncryptRequest:
    def __init__(self, plaintext, master_key_id, data_key_length):
        self.plaintext = plaintext
        self.master_key_id = master_key_id
        self.data_key_length = data_key_length


class SignOrVerifyRequest:
    def __init__(self, operation, key_id, message):
        self.operation = operation
        self.key_id = key_id
        self.message = message
