from pydantic import BaseModel
from typing import List, Union

class EmbeddingObject(BaseModel):
    index: int
    embedding: List[float]
    object: str

class EmbeddingResponse(BaseModel):
    data: List[EmbeddingObject]
    model: str
    object: str
    usage: dict

class EmbeddingRequest(BaseModel):
    input: Union[str, List[str]]
    model: str
    encoding_format: str = "float"