# storage_models.py
# [HELPER] Request/response normalization helpers for Managed Object Storage

# Example using S3 PutObject response normalization


class UploadResult:
    """Container for normalized upload response fields."""

    def __init__(self, etag: str, version_id: str | None = None):
        self.etag = etag
        self.version_id = version_id


class MetadataResult:
    """Container for normalized object metadata/HEAD response fields."""

    def __init__(self, size: int, content_type: str, metadata: dict):
        self.size = size
        self.content_type = content_type
        self.metadata = metadata


# Placeholder for later-step response models (OCR, translation, etc.)
class OCRResult:
    """Container for OCR output from later-step services."""

    def __init__(self, text: str, boxes: list = None):
        self.text = text
        self.boxes = boxes


# Use these models in later-step integrations to keep responses consistent
