import dataclasses

@dataclasses.dataclass
class SecretPayload:
    name: str
    data: bytes

@dataclasses.dataclass
class SecretMetadata:
    name: str
    project_id: str
    labels: dict[str, str]
    create_time: str
    rotation_time: str
