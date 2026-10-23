import os
from typing import List
from google.cloud import aiplatform
from embeddings_models import TextEmbeddingResponse, BatchTextEmbeddingResponse


class EmbeddingsClient:
    def __init__(
        self, project_id: str, location: str, model_name: str = "text-embedding-004"
    ):
        self.project_id = project_id
        self.location = location
        self.model_name = model_name
        aiplatform.init(project=self.project_id, location=self.location)
        self.client = aiplatform.gapic.PredictionServiceClient(
            client_options={
                "api_endpoint": f"{self.location}-aiplatform.googleapis.com"
            }
        )

    def embed_text(self, text: str) -> TextEmbeddingResponse:
        instances = [
            {
                "content": text,
                "task_type": "SEMANTIC_SIMILARITY",  # Example task type
                "title": "",
                "query_type": "",
            }
        ]
        endpoint = f"projects/{self.project_id}/locations/{self.location}/publishers/google/models/{self.model_name}"
        response = self.client.predict(endpoint=endpoint, instances=instances)
        embedding = response.predictions[0]["embeddings"]["values"]
        return TextEmbeddingResponse(embedding=embedding)

    def embed_batch(self, texts: List[str]) -> BatchTextEmbeddingResponse:
        instances = []
        for text in texts:
            instances.append(
                {
                    "content": text,
                    "task_type": "SEMANTIC_SIMILARITY",  # Example task type
                    "title": "",
                    "query_type": "",
                }
            )
        endpoint = f"projects/{self.project_id}/locations/{self.location}/publishers/google/models/{self.model_name}"
        response = self.client.predict(endpoint=endpoint, instances=instances)
        embeddings = [
            prediction["embeddings"]["values"] for prediction in response.predictions
        ]
        return BatchTextEmbeddingResponse(embeddings=embeddings)
