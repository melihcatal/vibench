from vertexai.language_models import TextEmbeddingModel
import os

def translation_memory_embedding(payload):
    model = TextEmbeddingModel.from_pretrained("text-embedding-004")
    segments = payload['segments'] # Expects a list of strings

    embeddings = model.get_embeddings(segments)
    
    embedding_vectors = [embedding.values for embedding in embeddings]

    return {"embeddings": embedding_vectors}
