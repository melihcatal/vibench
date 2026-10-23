from vertexai.language_models import TextEmbeddingModel

def embed_audit_notes(text):
    model = TextEmbeddingModel.from_pretrained("text-embedding-004")
    embeddings = model.get_embeddings([text])
    return [embedding.values for embedding in embeddings][0]
