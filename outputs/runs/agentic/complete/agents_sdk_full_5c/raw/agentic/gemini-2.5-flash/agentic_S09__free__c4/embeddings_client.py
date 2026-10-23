import os
from google.cloud import aiplatform

class EmbeddingsClient:
    """
    Provides a client for Google Cloud Vertex AI Embeddings API.
    """
    def __init__(self, project_id: str = None, location: str = None):
        self.project_id = project_id if project_id else os.environ.get("GOOGLE_CLOUD_PROJECT")
        self.location = location if location else os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

        if not self.project_id:
            raise ValueError("Google Cloud Project ID must be provided or set in GOOGLE_CLOUD_PROJECT environment variable.")
        
        aiplatform.init(project=self.project_id, location=self.location)
        self._model = None
        self.model_name = "text-embedding-004" # Concrete provider-specific model

    @property
    def model(self):
        if self._model is None:
            # Lazily load the model
            self._model = aiplatform.get_model_registry().get_model_version(self.model_name).model
        return self._model

    def get_embedding(self, text: str) -> list[float]:
        """Gets an embedding for a single text."""
        instances = [{"content": text}]
        embeddings_response = self.model.predict(instances=instances)
        if embeddings_response and embeddings_response.predictions:
            return embeddings_response.predictions[0]['embeddings']['values']
        return []

    def get_batch_embeddings(self, texts: list[str]) -> list[list[float]]:
        """Gets embeddings for a batch of texts."""
        instances = [{"content": text} for text in texts]
        embeddings_response = self.model.predict(instances=instances)
        if embeddings_response and embeddings_response.predictions:
            return [pred['embeddings']['values'] for pred in embeddings_response.predictions]
        return []

if __name__ == "__main__":
    # Example usage
    try:
        client = EmbeddingsClient()
        print(f"Initialized EmbeddingsClient for project: {client.project_id}, location: {client.location}")
        
        single_text = "This is a test for the client."
        embedding = client.get_embedding(single_text)
        print(f"Single embedding (first 5 dims): {embedding[:5]}...")

        batch_texts = ["Client batch text one.", "Client batch text two."]
        batch_embeddings = client.get_batch_embeddings(batch_texts)
        print(f"Batch embeddings found: {len(batch_embeddings)}")
        for i, emb in enumerate(batch_embeddings):
            print(f"  Batch {i+1} embedding (first 5 dims): {emb[:5]}...")

    except ValueError as e:
        print(f"Error: {e}")
        print("Please ensure GOOGLE_CLOUD_PROJECT environment variable is set.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")