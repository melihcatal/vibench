from pydantic import BaseModel, Field
from typing import Optional, List, Dict


# ---------- Request models ----------
class PutObjectRequest(BaseModel):
    Bucket: str = Field(..., description="Name of the bucket")
    Key: str = Field(..., description="Object key/path")
    Body: bytes = Field(..., description="File bytes or file path string")
    Metadata: Optional[Dict[str, str]] = Field(
        None, description="Optional user-defined metadata"
    )


class GeneratePresignedUrlRequest(BaseModel):
    ClientMethod: str = Field(..., description="API method, e.g., 'get_object'")
    Params: Dict[str, str] = Field(
        frozenset(), description="Parameters for the API call"
    )
    ExpiresIn: int = Field(3600, description="URL expiration in seconds")


# ---------- Response models ----------
class PutObjectResponse(BaseModel):
    ETAG: str = Field(..., description="ETag header returned by successful put")
    ContentLength: int = Field(..., description="Size of the uploaded object")

    class Config:
        use_enum_values = True

    def model_dump(self):
        return {"ETAG": self.ETAG, "ContentLength": self.ContentLength}


class HeadObjectResponse(BaseModel):
    LastModified: str = Field(..., description="Timestamp of last modification")
    ContentLength: int = Field(..., description="Size in bytes")
    ContentType: Optional[str] = Field(None, description="MIME type of object")
    Metadata: Optional[Dict[str, str]] = Field(None, description="User metadata")


class ListObjectsResponse(BaseModel):
    Contents: Optional[List[Dict[str, str]]] = Field(
        None, description="List of object summaries"
    )

    class Config:
        use_enum_values = True

    def model_dump(self):
        return {"Contents": self.Contents}
