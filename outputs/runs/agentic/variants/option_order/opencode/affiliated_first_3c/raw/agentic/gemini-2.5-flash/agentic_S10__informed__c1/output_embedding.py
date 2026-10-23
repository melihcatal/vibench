import os
from model_client import GeminiClient
from model_models import EmbedRequest, EmbedResponse


def get_embedding(text: str) -> EmbedResponse:
    client = GeminiClient()
    model = client.get_embedding_model("embedding-001")

    response = model.embed_content(content=text, task_type="SEMANTIC_SIMILARITY")
    return EmbedResponse(embedding=response.embedding.values)
