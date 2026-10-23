import os
from typing import Dict, Any
from openai import OpenAI
from security_models import EmbeddingResult


class CryptoAuditEmbedder:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model_id = "text-embedding-ada-002"

    def embed_crypto_audit_note(self, note: str) -> EmbeddingResult:
        try:
            response = self.client.embeddings.create(input=note, model=self.model_id)

            return EmbeddingResult(
                embedding=response.data[0].embedding,
                model_id=self.model_id,
                dimensions=len(response.data[0].embedding),
            )
        except Exception as e:
            raise Exception(f"Failed to embed crypto audit note: {e}")
