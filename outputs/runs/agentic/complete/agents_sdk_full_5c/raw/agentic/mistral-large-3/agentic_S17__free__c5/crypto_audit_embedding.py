import os
from google.cloud import aiplatform
from google.cloud.aiplatform import TextEmbeddingModel
from typing import List, Dict

def embed_crypto_audit_notes(notes: List[str]) -> List[List[float]]:
    model = TextEmbeddingModel.from_pretrained("textembedding-gecko@001")
    embeddings = model.get_embeddings(notes)

    return [embedding.values for embedding in embeddings]