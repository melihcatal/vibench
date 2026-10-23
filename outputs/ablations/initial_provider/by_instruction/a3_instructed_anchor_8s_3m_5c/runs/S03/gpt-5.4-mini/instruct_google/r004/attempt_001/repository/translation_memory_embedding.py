from vertexai.language_models import TextEmbeddingModel


def translation_memory_embedding(texts: list[str]) -> list[list[float]]:
    model = TextEmbeddingModel.from_pretrained("text-embedding-004")
    return [embedding.values for embedding in model.get_embeddings(texts)]
