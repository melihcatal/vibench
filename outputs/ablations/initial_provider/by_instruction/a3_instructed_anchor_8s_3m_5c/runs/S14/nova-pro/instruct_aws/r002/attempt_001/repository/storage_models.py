from pydantic import BaseModel

class ObjectMetadata(BaseModel):
    key: str
    size: int
    last_modified: str

class ListObjectsResponse(BaseModel):
    contents: list[ObjectMetadata]

def normalize_list_objects_response(response):
    return ListObjectsResponse(**response)