import os
import vertexai
from vertexai.preview.generative_models import TextEmbeddingModel
from model_models import EmbeddingRequest, EmbeddingResponse
from typing import List


class VertexAITextEmbeddingClient:
    def __init__(self):
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
        location = os.getenv("GOOGLE_CLOUD_LOCATION")
        if not project_id or not location:
            raise ValueError(
                "GOOGLE_CLOUD_PROJECT_ID and GOOGLE_CLOUD_LOCATION environment variables must be set."
            )
        vertexai.init(project=project_id, location=location)
        self.model = TextEmbeddingModel.from_pretrained(
            "text-embedding-004"
        )  # Concrete model identifier

    def embed_text(self, request: EmbeddingRequest) -> EmbeddingResponse:
        if not request.texts:
            return EmbeddingResponse(embeddings=[])

        embeddings_response = self.model.embed(request.texts)
        # The response structure is a list of Embedding objects, each containing a list of floats
        # We need to extract the actual embedding vectors (list of floats)
        embeddings = [embedding.values for embedding in embeddings_response]
        return EmbeddingResponse(embeddings=embeddings)


def get_output_embeddings(request: EmbeddingRequest) -> EmbeddingResponse:
    client = VertexAITextEmbeddingClient()
    return client.embed_text(request)
