from typing import TypedDict, Dict, List


class CryptoEvent(TypedDict):
    timestamp: str
    operation: str
    key_id: str
    status: str


EnvelopeCiphertext: TypedDict = Dict[str, bytes]
