import dataclasses


@dataclasses.dataclass
class SecretIdentifier:
    """
    Defines a structure for identifying a secret in Google Secret Manager.
    Provider: Google Cloud Secret Manager
    """

    project_id: str
    secret_id: str
    version_id: str = "latest"

    def to_resource_name(self) -> str:
        return f"projects/{self.project_id}/secrets/{self.secret_id}/versions/{self.version_id}"


@dataclasses.dataclass
class ModerationResult:
    """
    Defines a structure for content moderation results.
    Provider: Perspective API
    """

    is_safe: bool
    scores: dict
    attribute_scores: dict
