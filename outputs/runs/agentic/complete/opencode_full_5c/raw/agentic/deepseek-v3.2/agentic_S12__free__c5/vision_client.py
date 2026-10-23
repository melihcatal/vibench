import os
from typing import Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class VisionConfig:
    """Configuration for vision service clients."""

    google_credentials_path: Optional[str] = None
    openai_api_key: Optional[str] = None
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    aws_region: Optional[str] = None
    azure_content_safety_endpoint: Optional[str] = None
    azure_content_safety_key: Optional[str] = None

    @classmethod
    def from_env(cls) -> "VisionConfig":
        """Load configuration from environment variables."""
        return cls(
            google_credentials_path=os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"),
            openai_api_key=os.environ.get("OPENAI_API_KEY"),
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
            aws_region=os.environ.get("AWS_REGION", "us-east-1"),
            azure_content_safety_endpoint=os.environ.get(
                "AZURE_CONTENT_SAFETY_ENDPOINT"
            ),
            azure_content_safety_key=os.environ.get("AZURE_CONTENT_SAFETY_KEY"),
        )

    def validate(self) -> None:
        """Validate that required configuration is present."""
        errors = []

        if not self.google_credentials_path and not os.environ.get(
            "GOOGLE_APPLICATION_CREDENTIALS"
        ):
            errors.append("Google Cloud credentials not configured")

        if not self.openai_api_key:
            errors.append("OpenAI API key not configured")

        if not (self.aws_access_key_id and self.aws_secret_access_key):
            errors.append("AWS credentials not configured")

        if not (self.azure_content_safety_endpoint and self.azure_content_safety_key):
            errors.append("Azure Content Safety configuration not complete")

        if errors:
            raise ValueError(f"Configuration errors: {', '.join(errors)}")


def load_image_bytes(image_path: str) -> bytes:
    """Load image file as bytes."""
    with open(image_path, "rb") as f:
        return f.read()


def normalize_confidence_score(score: float, source: str) -> float:
    """Normalize confidence scores from different providers to 0-1 range."""
    if source == "google":
        return score  # Google already returns 0-1
    elif source == "aws":
        return score / 100.0  # AWS returns 0-100
    elif source == "azure":
        return score / 10.0  # Azure returns 0-10
    else:
        return score
