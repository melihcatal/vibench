from vertexai.language_models import TextEmbeddingModel


def log_embedding(text):
    model = TextEmbeddingModel.from_pretrained("text-embedding-004")
    embeddings = model.get_embeddings([text])
    return embeddings[0].values
