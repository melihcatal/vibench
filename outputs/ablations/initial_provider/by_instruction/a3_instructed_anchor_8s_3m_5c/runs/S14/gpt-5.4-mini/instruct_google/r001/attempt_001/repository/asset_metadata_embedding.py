from google.cloud import aiplatform


def asset_metadata_embedding(text: str):
    aiplatform.init()
    model = aiplatform.TextEmbeddingModel.from_pretrained("text-embedding-004")
    return model.get_embeddings([text])[0].values
