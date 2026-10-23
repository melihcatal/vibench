# [HELPER] storage_models.py

# Provider: Amazon S3
# SDK: boto3
# Auth: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

from typing import TypedDict, Optional


# Response model for listing objects
class ListObjectsResponse(TypedDict):
    Keys: list[str]
    ContinuationToken: Optional[str]


# Normalized metadata model used across helper functions
class ObjectMetadata(TypedDict):
    Key: str
    Size: int
    LastModified: str  # ISO 8601 string
    ContentType: Optional[str]


# Simple request DTO for upload (file path or raw bytes)
UploadedData = TypedDict(
    "UploadedData",
    {
        "file_path": str,
    },
    total=False,
)

# You can add additional models (search embeddings, OCR results) here as needed
