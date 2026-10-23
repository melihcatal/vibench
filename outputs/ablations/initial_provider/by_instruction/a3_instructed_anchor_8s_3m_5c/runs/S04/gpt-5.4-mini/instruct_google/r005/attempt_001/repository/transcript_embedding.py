from vertexai.language_models import TextEmbeddingModel


def transcript_embedding(text: str):
    model = TextEmbeddingModel.from_pretrained("text-embedding-004")
    return model.get_embeddings([text])[0].values
