import ibm_watsonx_ai
from ibm_watsonx_ai.services.embedding import EmbeddingService
import os


class Embedder:
    def __init__(self):
        api_key = os.getenv("WATSONX_API_KEY")
        project_id = os.getenv("WATSONX_PROJECT_ID")
        self.service = EmbeddingService(api_key=api_key, project_id=project_id)

    def embed(self, texts: List[str]) -> List[List[float]]:
        """Embed a list of text segments using IBM WatsonX embeddings."""
        response = self.service.embed_text(texts=texts)
        # Assume response returns embeddings in the order provided
        return [vec["embedding"] for vec in response]


if __name__ == "__main__":
    vecs = Embedder().embed(["Hello world", "Bonjour le monde"])
    print(vecs)
