import os
from dataclasses import dataclass
import cohere

@dataclass
class EmbeddingRequest:
    texts: list[str]
    model: str = "embed-english-v3.0" # A common embedding model from Cohere

@dataclass
class EmbeddingResponse:
    embeddings: list[list[float]]
    texts: list[str]

class TranslationMemoryEmbedder:
    def __init__(self):
        self.client = cohere.Client(os.environ.get("COHERE_API_KEY"))
        if not self.client.api_key:
            raise ValueError("COHERE_API_KEY environment variable not set.")

    def embed_segments(self, request: EmbeddingRequest) -> EmbeddingResponse:
        if not request.texts:
            return EmbeddingResponse(embeddings=[], texts=[])

        response = self.client.embed(
            texts=request.texts,
            model=request.model,
            input_type="search_document" # Or "search_query", "classification", etc. depending on use-case
        )
        
        # Cohere's embed returns a 'embeddings' field which is a list of lists of floats
        return EmbeddingResponse(
            embeddings=response.embeddings,
            texts=request.texts
        )
