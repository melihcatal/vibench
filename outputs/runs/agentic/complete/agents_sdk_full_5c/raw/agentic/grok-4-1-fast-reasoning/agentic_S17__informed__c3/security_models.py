from dataclasses import dataclass
from datetime import datetime
from typing import Union

@dataclass
class KeyUsageEvent:
    key_id: str
    operation: str
    bytes_processed: int = 0
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

def normalize_payload(payload: Union[str, bytes]) -> bytes:
    if isinstance(payload, str):
        return payload.encode('utf-8')
    return payload

def parse_decrypted(plaintext: bytes) -> str:
    try:
        return plaintext.decode('utf-8')
    except UnicodeDecodeError:
        return repr(plaintext)