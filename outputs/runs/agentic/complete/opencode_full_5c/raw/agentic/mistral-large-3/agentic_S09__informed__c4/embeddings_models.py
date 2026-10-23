from typing import List, Union
from pydantic import BaseModel


class EmbeddingObject(BaseModel):
    object: str
    embedding: List[float]
    index: int


class EmbeddingResponse(BaseModel):
    object: str
    data: List[EmbeddingObject]
    model: str
    usage: dict


class EmbeddingRequest(BaseModel):
    input: Union[str, List[str]]
    model: str
    encoding_format: Optional[str] = "float"
    dimensions: Optional[int] = None
    user: Optional[str] = None

    def dict(self, **kwargs):
        data = super().dict(**kwargs)
        # Remove None values to avoid sending optional fields as null
        return {k: v for k, v in data.items() if v is not None}
