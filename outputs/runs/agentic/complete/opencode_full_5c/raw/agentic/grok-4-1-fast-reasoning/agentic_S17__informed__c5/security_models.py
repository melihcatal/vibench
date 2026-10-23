from dataclasses import dataclass


@dataclass
class Envelope:
    encrypted_data: bytes
    encrypted_key: bytes
