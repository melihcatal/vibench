import cohere
import os


class SecretAuditEmbedder:
    def __init__(self):
        self.api_key = os.getenv("COHERE_API_KEY")
        if not self.api_key:
            raise ValueError("COHERE_API_KEY environment variable is not set")
        self.client = cohere.Client(self.api_key)

    def embed_secret_audit_notes(self, text: str) -> List[float]:
        response = self.client.embed(texts=[text], model="embed-english-v3.0")
        return response.embeddings[0]
