from pydantic import BaseModel

class EmbeddingRequest(BaseModel):
    input: str

class EmbeddingResponse(BaseModel):
    embedding: list

def normalize_embedding_response(response):
    return EmbeddingResponse(embedding=response['data'][0]['embedding']).dict()