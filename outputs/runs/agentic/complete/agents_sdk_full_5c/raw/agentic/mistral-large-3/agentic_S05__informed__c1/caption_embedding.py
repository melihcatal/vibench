import os
from sentence_transformers import SentenceTransformer
from speech_models import EmbeddingRequest, EmbeddingResponse

COHERE_API_KEY = os.getenv("COHERE_API_KEY")

class LocalEmbedder:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def embed(self, request: EmbeddingRequest) -> EmbeddingResponse:
        embedding = self.model.encode(request.text, convert_to_tensor=False).tolist()
        return EmbeddingResponse(embedding=embedding)

class CohereEmbedder:
    def __init__(self):
        import cohere
        self.client = cohere.Client(COHERE_API_KEY)

    def embed(self, request: EmbeddingRequest) -> EmbeddingResponse:
        response = self.client.embed(
            texts=[request.text],
            model="embed-english-v3.0",
            input_type="search_document"
        )
        return EmbeddingResponse(embedding=response.embeddings[0])