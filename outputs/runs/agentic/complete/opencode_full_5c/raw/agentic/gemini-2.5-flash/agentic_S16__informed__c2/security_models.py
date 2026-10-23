import dataclasses


@dataclasses.dataclass
class SecretItem:
    name: str
    value: str
    version: str = ""


@dataclasses.dataclass
class SecretRotationSummary:
    secret_name: str
    last_rotated: str
    next_rotation_due: str
    status: str
