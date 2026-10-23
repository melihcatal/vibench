from dataclasses import dataclass


@dataclass
class SecretValue:
    name: str
    value: str
    version: str
