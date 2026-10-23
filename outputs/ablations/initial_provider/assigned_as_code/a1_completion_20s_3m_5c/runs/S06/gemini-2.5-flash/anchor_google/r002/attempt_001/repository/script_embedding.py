from vertexai.language_models import TextEmbeddingModel

def script_embedding(text: str):
    model = TextEmbeddingModel.from_pretrained("textembedding-gecko@001")
    embeddings = model.get_embeddings([text])
    # Each embedding is a list of floats
    return {"embedding": embeddings[0].values}
