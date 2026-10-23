import dataclasses

@dataclasses.dataclass
class Secret:
    project_id: str
    secret_id: str
    version_id: str
    payload: str
