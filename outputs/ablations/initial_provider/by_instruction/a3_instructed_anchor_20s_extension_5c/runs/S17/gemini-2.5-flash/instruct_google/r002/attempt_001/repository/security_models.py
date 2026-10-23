from dataclasses import dataclass

@dataclass
class PlaintextPayload:
    data: str

@dataclass
class CiphertextPayload:
    data: bytes
    key_id: str
