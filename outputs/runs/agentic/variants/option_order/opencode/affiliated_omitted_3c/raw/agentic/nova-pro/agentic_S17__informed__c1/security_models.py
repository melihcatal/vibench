class EncryptRequest:
    def __init__(self, project_id, location_id, key_ring_id, key_id, plaintext):
        self.project_id = project_id
        self.location_id = location_id
        self.key_ring_id = key_ring_id
        self.key_id = key_id
        self.plaintext = plaintext


class DecryptRequest:
    def __init__(self, project_id, location_id, key_ring_id, key_id, ciphertext):
        self.project_id = project_id
        self.location_id = location_id
        self.key_ring_id = key_ring_id
        self.key_id = key_id
        self.ciphertext = ciphertext
