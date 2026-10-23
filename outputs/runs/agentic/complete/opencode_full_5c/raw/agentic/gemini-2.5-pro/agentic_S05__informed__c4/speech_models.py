from dataclasses import dataclass


@dataclass
class Caption:
    text: str
    is_final: bool
    speaker: int = 0
