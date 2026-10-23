from vertexai.language_models import TextEmbeddingModel

def get_text_embedding(text: str) -> list[float]:
    model = TextEmbeddingModel.from_pretrained("textembedding-gecko@003")
    embeddings = model.get_embeddings([text])
    return embeddings[0].values
