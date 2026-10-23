import os
from typing import List, Dict, Any

from google.cloud import aiplatform

class EmbeddingsClient:
    def __init__(self, project_id: str = None, location: str = "us-central1"):
        if project_id is None:
            project_id = os.getenv("GCP_PROJECT_ID")
            if not project_id:
                raise ValueError("GCP_PROJECT_ID not set as environment variable or provided.")
        self.project_id = project_id
        self.location = location
        # Initialize Vertex AI SDK
        aiplatform.init(project=self.project_id, location=self.location)
        self._model = None # To store the model once loaded

    def _get_model(self, model_name: str):
        if self._model is None or self._model.model_id != model_name:
            # Load the model. For text embeddings, it's typically 'text-embedding-004' or 'text-embedding-gecko@001'
            self._model = aiplatform.TextEmbeddingModel.from_pretrained(model_name)
        return self._model

    def get_embedding(self, text: str, model_name: str = "text-embedding-004") -> List[float]:
        model = self._get_model(model_name)
        embeddings = model.get_embeddings([text])
        return embeddings[0].values

    def get_batch_embeddings(self, texts: List[str], model_name: str = "text-embedding-004") -> List[List[float]]:
        model = self._get_model(model_name)
        embeddings = model.get_embeddings(texts)
        return [e.values for e in embeddings]
