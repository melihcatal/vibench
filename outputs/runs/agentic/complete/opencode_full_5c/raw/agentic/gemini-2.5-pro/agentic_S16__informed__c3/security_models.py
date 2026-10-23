import dataclasses


@dataclasses.dataclass
class SecretPayload:
    project_id: str
    secret_id: str
    version_id: str = "latest"
