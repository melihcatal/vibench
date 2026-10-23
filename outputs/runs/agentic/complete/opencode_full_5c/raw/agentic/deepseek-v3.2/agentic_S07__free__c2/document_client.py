import os
import json
from typing import Dict, Any, Optional, Union
from dataclasses import dataclass, asdict
import base64


@dataclass
class DocumentConfig:
    """Configuration for document processing services."""

    google_vision_credentials: Optional[str] = None
    azure_vision_endpoint: Optional[str] = None
    azure_vision_key: Optional[str] = None
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    aws_region: Optional[str] = None
    google_project_id: Optional[str] = None
    google_processor_id: Optional[str] = None
    openai_api_key: Optional[str] = None
    cohere_api_key: Optional[str] = None

    @classmethod
    def from_env(cls) -> "DocumentConfig":
        """Create configuration from environment variables."""
        return cls(
            google_vision_credentials=os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"),
            azure_vision_endpoint=os.environ.get("AZURE_VISION_ENDPOINT"),
            azure_vision_key=os.environ.get("AZURE_VISION_KEY"),
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
            aws_region=os.environ.get("AWS_REGION"),
            google_project_id=os.environ.get("GOOGLE_CLOUD_PROJECT"),
            google_processor_id=os.environ.get("DOCUMENT_AI_PROCESSOR_ID"),
            openai_api_key=os.environ.get("OPENAI_API_KEY"),
            cohere_api_key=os.environ.get("COHERE_API_KEY"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)

    def validate(self) -> bool:
        """Validate that required configuration is present."""
        required_configs = [
            (self.google_vision_credentials, "Google Vision credentials"),
            (
                self.azure_vision_endpoint and self.azure_vision_key,
                "Azure Vision configuration",
            ),
            (self.aws_access_key_id and self.aws_secret_access_key, "AWS credentials"),
            (
                self.google_project_id and self.google_processor_id,
                "Google Document AI configuration",
            ),
        ]

        has_at_least_one = any(config[0] for config in required_configs)
        return has_at_least_one


class DocumentClient:
    """Client helper for document processing services."""

    def __init__(self, config: Optional[DocumentConfig] = None):
        self.config = config or DocumentConfig.from_env()

    def load_image_as_base64(self, image_path: str) -> str:
        """Load image file and encode as base64."""
        with open(image_path, "rb") as image_file:
            image_bytes = image_file.read()
        return base64.b64encode(image_bytes).decode("utf-8")

    def load_image_bytes(self, image_path: str) -> bytes:
        """Load image file as bytes."""
        with open(image_path, "rb") as image_file:
            return image_file.read()

    def save_result(self, result: Any, output_path: str) -> None:
        """Save processing result to JSON file."""
        if isinstance(result, dict):
            data = result
        else:
            data = {"result": str(result)}

        with open(output_path, "w") as f:
            json.dump(data, f, indent=2)

    def normalize_text(self, text: str) -> str:
        """Normalize extracted text."""
        import re

        text = text.strip()
        text = re.sub(r"\s+", " ", text)
        text = re.sub(r"\n\s*\n", "\n\n", text)
        return text

    def extract_metadata(self, image_path: str) -> Dict[str, Any]:
        """Extract basic metadata from image file."""
        import os
        from PIL import Image

        metadata = {
            "filename": os.path.basename(image_path),
            "filesize": os.path.getsize(image_path),
            "filetype": os.path.splitext(image_path)[1].lower(),
        }

        try:
            with Image.open(image_path) as img:
                metadata.update(
                    {
                        "width": img.width,
                        "height": img.height,
                        "mode": img.mode,
                        "format": img.format,
                    }
                )
        except Exception:
            pass

        return metadata

    def create_batch_request(self, image_paths: List[str]) -> List[Dict[str, Any]]:
        """Create batch processing request for multiple images."""
        requests = []
        for image_path in image_paths:
            with open(image_path, "rb") as f:
                image_bytes = f.read()

            request = {
                "path": image_path,
                "bytes": base64.b64encode(image_bytes).decode("utf-8"),
                "metadata": self.extract_metadata(image_path),
            }
            requests.append(request)

        return requests

    def validate_service_availability(self) -> Dict[str, bool]:
        """Check which document processing services are available."""
        availability = {
            "google_vision": bool(self.config.google_vision_credentials),
            "azure_vision": bool(
                self.config.azure_vision_endpoint and self.config.azure_vision_key
            ),
            "aws_textract": bool(
                self.config.aws_access_key_id and self.config.aws_secret_access_key
            ),
            "google_document_ai": bool(
                self.config.google_project_id and self.config.google_processor_id
            ),
            "openai": bool(self.config.openai_api_key),
            "cohere": bool(self.config.cohere_api_key),
        }

        return availability
