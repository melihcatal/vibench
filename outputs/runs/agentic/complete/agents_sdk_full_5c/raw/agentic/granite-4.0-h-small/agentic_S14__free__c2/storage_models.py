from typing import Dict, Any

class StorageUploadResponse(Dict[str, Any]):
    """Normalized response type for object upload."""
    pass

class StoragePresignResponse(Dict[str, Any]):
    """Normalized response type for presigned URL generation."""
    pass

class StorageMetadataResponse(Dict[str, Any]):
    """Normalized response type for object metadata retrieval."""
    pass
