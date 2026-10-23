from pydantic import BaseModel, Field

class ObjectMetadata(BaseModel):
    key: str = Field(..., description="Object key (path) in the bucket")
    last_modified: str = Field(None, description="ISO 8601 timestamp of last modification")
    content_length: int = Field(None, description="Size in bytes")
    content_type: str = Field(None, description="MIME type of the object")
    metadata: dict = Field({}, description="User-defined metadata")

class ListResult(BaseModel):
    keys: list[str] = Field([], description="List of object keys matching the request")
    continuation_token: str = Field(None, description="Token for pagination")
