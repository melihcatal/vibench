from sentence_transformers import SentenceTransformer
import numpy as np
import json


# Provider: Sentence Transformers (Hugging Face)
# Model: all-MiniLM-L6-v2
class CryptoAuditEmbedder:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def embed_crypto_audit_note(self, note: str) -> dict:
        embedding = self.model.encode(note, convert_to_tensor=True)
        return {
            "embedding": embedding.cpu().numpy().tolist(),
            "model": "all-MiniLM-L6-v2",
            "provider": "sentence_transformers",
        }


def embed_crypto_audit_note(note: str) -> dict:
    embedder = CryptoAuditEmbedder()
    return embedder.embed_crypto_audit_note(note)
