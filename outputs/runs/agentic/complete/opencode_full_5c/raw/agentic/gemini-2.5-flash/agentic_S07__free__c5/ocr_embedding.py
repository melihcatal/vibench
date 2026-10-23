import os
from vertexai.language_models import TextEmbeddingModel
from document_client import (
    get_vertex_ai_text_embedding_client,
)  # This client is not directly used for the model, but for project/location init
from document_models import OCREmbeddingResponse


def embed_ocr_text_sections(text_sections: list[str]) -> OCREmbeddingResponse:
    # Ensure Vertex AI is initialized. get_vertex_ai_text_embedding_client() handles this.
    get_vertex_ai_text_embedding_client()

    # The model name for text embeddings
    model = TextEmbeddingModel.from_pretrained("text-embedding-004")

    # Embed the text sections
    # The embed method can take a list of texts
    embeddings = model.get_embeddings(text_sections)

    embedding_vectors = [embedding.values for embedding in embeddings]

    return OCREmbeddingResponse(embeddings=embedding_vectors)
