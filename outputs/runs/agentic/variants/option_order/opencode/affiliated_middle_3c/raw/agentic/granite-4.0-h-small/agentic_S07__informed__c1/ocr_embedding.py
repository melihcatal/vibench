import os
import dashscope
from document_client import DocumentClient
from document_models import EmbedDocumentRequest, EmbedDocumentResponse


class EmbedDocument:
    def __init__(self):
        # DashScope client initialized with API key from env variable
        dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")
        self.document_client = DocumentClient()
        self.embeddings_model = "qwen2.5-1.8B"

    def embed(self, text: str) -> EmbedDocumentResponse:
        """Embed extracted document sections for semantic retrieval using DashScope embeddings.

        Args:
            text: Text to be embedded.

        Returns:
            EmbedDocumentResponse containing the embedding vector.
        """
        payload = {"model": self.embeddings_model, "inputs": [text]}
        response = dashscope.embeddings.create(**payload)
        vector = response.result[0]["embedding"]
        return EmbedDocumentResponse(embedding=vector)


if __name__ == "__main__":
    embedder = EmbedDocument()
    result = embedder.embed("Learning to extract meaningful embeddings from documents.")
    print(result.embedding)
