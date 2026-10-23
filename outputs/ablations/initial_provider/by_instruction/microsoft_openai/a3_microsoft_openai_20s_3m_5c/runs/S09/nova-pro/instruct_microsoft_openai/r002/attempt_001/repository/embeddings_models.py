from typing import List

class EmbeddingRequest:
  def __init__(self, input: str):
    self.input = input

class EmbeddingResponse:
  def __init__(self, embedding: List[float]):
    self.embedding = embedding

def normalize_response(response) -> EmbeddingResponse:
  return EmbeddingResponse(response.data[0].embedding)